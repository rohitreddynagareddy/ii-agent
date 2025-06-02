from argparse import ArgumentParser
import uuid
from pathlib import Path
from ii_agent.utils import WorkspaceManager


def parse_common_args(parser: ArgumentParser):
    parser.add_argument(
        "--workspace",
        type=str,
        default="./workspace",
        help="Path to the workspace",
    )
    parser.add_argument(
        "--logs-path",
        type=str,
        default="agent_logs.txt",
        help="Path to save logs",
    )
    parser.add_argument(
        "--needs-permission",
        "-p",
        help="Ask for permission before executing commands",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--use-container-workspace",
        type=str,
        default=None,
        help="(Optional) Path to the container workspace to run commands in.",
    )
    parser.add_argument(
        "--docker-container-id",
        type=str,
        default=None,
        help="(Optional) Docker container ID to run commands in.",
    )
    parser.add_argument(
        "--minimize-stdout-logs",
        help="Minimize the amount of logs printed to stdout.",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--project-id",
        type=str,
        default=None,
        help="Project ID to use for Anthropic",
    )
    parser.add_argument(
        "--region",
        type=str,
        default=None,
        help="Region to use for Anthropic",
    )
    parser.add_argument(
        "--context-manager",
        type=str,
        default="llm-summarizing",
        choices=["llm-summarizing", "amortized-forgetting"],
        help="Type of context manager to use (llm-summarizing, or amortized-forgetting)",
    )
    parser.add_argument(
        "--memory-tool",
        type=str,
        default="compactify-memory",
        choices=["compactify-memory", "none", "simple"],
        help="Type of memory tool to use"
    )
    return parser


def create_workspace_manager_for_connection(
    workspace_root: str, use_container_workspace: bool = False
):
    """Create a new workspace manager instance for a websocket connection."""
    # Create unique subdirectory for this connection
    connection_id = str(uuid.uuid4())
    workspace_path = Path(workspace_root).resolve()
    connection_workspace = workspace_path / connection_id
    connection_workspace.mkdir(parents=True, exist_ok=True)

    # Initialize workspace manager with connection-specific subdirectory
    workspace_manager = WorkspaceManager(
        root=connection_workspace,
        container_workspace=use_container_workspace,
    )

    return workspace_manager, connection_id
