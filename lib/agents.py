from typing import TypedDict, List, Optional, Union
import json

from lib.state_machine import StateMachine, Step, EntryPoint, Termination, Run
from lib.llm import LLM
from lib.messages import AIMessage, UserMessage, SystemMessage, ToolMessage
from lib.tooling import Tool, ToolCall
from lib.memory import ShortTermMemory


# Define the state schema
class AgentState(TypedDict):
    user_query: str                     # Current user query
    instructions: str                   # System instructions
    messages: List[dict]                # Conversation history
    current_tool_calls: Optional[List[ToolCall]]  # Pending tool calls
    total_tokens: int                   # Cumulative token count
    session_id: str                     # ✅ Session identifier


class Agent:
    def __init__(
        self,
        model_name: str,
        instructions: str,
        tools: List[Tool] = None,
        temperature: float = 0.7
    ):
        """
        Initialize an Agent
        """
        self.instructions = instructions
        self.tools = tools if tools else []
        self.model_name = model_name
        self.temperature = temperature

        # Initialize memory and workflow
        self.memory = ShortTermMemory()
        self.workflow = self._create_state_machine()

    def _prepare_messages_step(self, state: AgentState) -> AgentState:
        """Prepare messages for LLM consumption"""
        messages = state.get("messages", [])

        # Initialize with system message if empty
        if not messages:
            messages = [SystemMessage(content=state["instructions"])]

        # Append current user query
        messages.append(UserMessage(content=state["user_query"]))

        return {
            **state,                 # ✅ Preserve session + tokens
            "messages": messages,
        }

    def _llm_step(self, state: AgentState) -> AgentState:
        """Process state through the LLM"""
        llm = LLM(
            model=self.model_name,
            temperature=self.temperature,
            tools=self.tools,
        )

        response = llm.invoke(state["messages"])
        tool_calls = response.tool_calls if response.tool_calls else None

        # Update token usage
        total_tokens = state.get("total_tokens", 0)
        if response.token_usage:
            total_tokens += response.token_usage.total_tokens

        ai_message = AIMessage(
            content=response.content,
            tool_calls=tool_calls,
        )

        return {
            **state,                 # ✅ Preserve session
            "messages": state["messages"] + [ai_message],
            "current_tool_calls": tool_calls,
            "total_tokens": total_tokens,
        }

    def _tool_step(self, state: AgentState) -> AgentState:
        """Execute pending tool calls"""
        tool_calls = state["current_tool_calls"] or []
        tool_messages = []

        for call in tool_calls:
            function_name = call.function.name
            function_args = json.loads(call.function.arguments)
            tool_call_id = call.id

            tool = next((t for t in self.tools if t.name == function_name), None)
            if tool:
                result = str(tool(**function_args))
                tool_messages.append(
                    ToolMessage(
                        content=json.dumps(result),
                        tool_call_id=tool_call_id,
                        name=function_name,
                    )
                )

        return {
            **state,                 # ✅ Preserve session + tokens
            "messages": state["messages"] + tool_messages,
            "current_tool_calls": None,
        }

    def _create_state_machine(self) -> StateMachine[AgentState]:
        """Create the agent state machine"""
        machine = StateMachine[AgentState](AgentState)

        entry = EntryPoint[AgentState]()
        message_prep = Step("message_prep", self._prepare_messages_step)
        llm_processor = Step("llm_processor", self._llm_step)
        tool_executor = Step("tool_executor", self._tool_step)
        termination = Termination[AgentState]()

        machine.add_steps([
            entry,
            message_prep,
            llm_processor,
            tool_executor,
            termination,
        ])

        machine.connect(entry, message_prep)
        machine.connect(message_prep, llm_processor)

        def check_tool_calls(state: AgentState) -> Union[Step[AgentState], str]:
            if state.get("current_tool_calls"):
                return tool_executor
            return termination

        machine.connect(llm_processor, [tool_executor, termination], check_tool_calls)
        machine.connect(tool_executor, llm_processor)

        return machine

    def invoke(self, query: str, session_id: Optional[str] = None) -> Run:
        """
        Run the agent for a given query and session
        """
        session_id = session_id or "default"

        # Ensure session exists
        self.memory.create_session(session_id)

        # Retrieve previous context
        previous_messages = []
        last_run: Run = self.memory.get_last_object(session_id)
        if last_run:
            last_state = last_run.get_final_state()
            if last_state:
                previous_messages = last_state["messages"]

        initial_state: AgentState = {
            "user_query": query,
            "instructions": self.instructions,
            "messages": previous_messages,
            "current_tool_calls": None,
            "total_tokens": 0,        # ✅ Explicit initialization
            "session_id": session_id,
        }

        run_object = self.workflow.run(initial_state)

        # Persist run in session memory
        self.memory.add(run_object, session_id)

        return run_object

    def get_session_runs(self, session_id: Optional[str] = None) -> List[Run]:
        """Retrieve all runs for a session"""
        return self.memory.get_all_objects(session_id)

    def reset_session(self, session_id: Optional[str] = None):
        """Reset a session's memory"""
        self.memory.reset(session_id)
