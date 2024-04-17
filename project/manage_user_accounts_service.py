from typing import Optional

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class ManageUserAccountsResponse(BaseModel):
    """
    Provides feedback on the outcome of the manage user accounts request; includes status of operation and any applicable messages.
    """

    message: str
    isSuccess: bool


async def manage_user_accounts(
    userId: str, newRole: prisma.enums.UserRole, isActive: Optional[bool]
) -> ManageUserAccountsResponse:
    """
    Endpoint for admin roles to manage user accounts and roles.

    Args:
    userId (str): The unique identifier of the user whose account is to be managed.
    newRole (UserRole): The new role to assign to the user.
    isActive (Optional[bool]): Flag indicating whether the user account is to be activated or deactivated.

    Returns:
    ManageUserAccountsResponse: Provides feedback on the outcome of the manage user accounts request; includes status of operation and any applicable messages.
    """
    user = await prisma.models.User.prisma().find_unique(where={"id": userId})
    if not user:
        return ManageUserAccountsResponse(
            message=f"User with ID {userId} not found.", isSuccess=False
        )
    update_data = {"role": newRole}
    if isActive is not None:
        update_data["isActive"] = isActive
    try:
        updated_user = await prisma.models.User.prisma().update(
            where={"id": userId}, data=update_data
        )
        return ManageUserAccountsResponse(
            message=f"User with ID {userId} successfully updated.", isSuccess=True
        )
    except Exception as e:
        return ManageUserAccountsResponse(
            message=f"Failed to update user with ID {userId}. Error: {str(e)}",
            isSuccess=False,
        )
