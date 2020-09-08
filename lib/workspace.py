from lib.api_call import RequestTypes
from lib.clockify_api_call import ClockifyApiCall


class Workspace:

    def __init__(self, name: str, workspace_id: str):
        self.name = name
        self.id = workspace_id

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    @staticmethod
    def get_all():
        """
        Gets all Workspaces

        Returns:
            Workspace[]: List of all Workspaces
        """
        workspace_jsons = ClockifyApiCall(RequestTypes.GET, "workspaces").exec().json()

        workspaces = []

        for workspace_json in workspace_jsons:
            workspaces.append(Workspace._get_from_json(workspace_json))

        return workspaces

    @staticmethod
    def _get_from_json(json: dict):
        """
        Given a JSON representation of a Workspace (typically, from a REST API call), return a Workspace object

        Args:
            json (dict): JSON representation of a Workspace

        Returns:
            Workspace: Workspace object represented by the JSON
        """
        name = json["name"]
        workspace_id = json["id"]

        return Workspace(name, workspace_id)
