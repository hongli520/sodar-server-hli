import rules

# Projectroles dependency
from projectroles import rules as pr_rules  # To access common predicates


# Predicates -------------------------------------------------------------------


# TODO: If we need to assign new predicates, we do it here


# Rules ------------------------------------------------------------------------


# TODO: Rules should not be needed, use permissions for user rights


# Permissions ------------------------------------------------------------------


# Allow viewing and listing user's own landing zones for the project
rules.add_perm(
    'landingzones.view_zone_own',
    pr_rules.is_project_owner
    | pr_rules.is_project_delegate
    | pr_rules.is_project_contributor,
)

# Allow viewing and listing all landing zones for the project
rules.add_perm(
    'landingzones.view_zone_all',
    pr_rules.is_project_owner | pr_rules.is_project_delegate,
)

# Allow creating landing zones
rules.add_perm(
    'landingzones.create_zone',
    pr_rules.can_modify_project_data
    & (
        pr_rules.is_project_owner
        | pr_rules.is_project_delegate
        | pr_rules.is_project_contributor
    ),
)

# Allow updating the user's own landing zones
rules.add_perm(
    'landingzones.update_zone_own',
    pr_rules.can_modify_project_data
    & (
        pr_rules.is_project_owner
        | pr_rules.is_project_delegate
        | pr_rules.is_project_contributor
    ),
)

# Allow moving files from the user's own landing zones
rules.add_perm(
    'landingzones.move_zone_own',
    pr_rules.can_modify_project_data
    & (
        pr_rules.is_project_owner
        | pr_rules.is_project_delegate
        | pr_rules.is_project_contributor
    ),
)

# Allow deleting the user's own landing zones
# NOTE: Is allowed if project is archived
rules.add_perm(
    'landingzones.delete_zone_own',
    pr_rules.is_project_owner
    | pr_rules.is_project_delegate
    | pr_rules.is_project_contributor,
)

# Allow updating any landing zone
rules.add_perm(
    'landingzones.update_zone_all',
    pr_rules.can_modify_project_data
    & (pr_rules.is_project_owner | pr_rules.is_project_delegate),
)

# Allow moving files from any landing zone
rules.add_perm(
    'landingzones.move_zone_all',
    pr_rules.can_modify_project_data
    & (pr_rules.is_project_owner | pr_rules.is_project_delegate),
)

# Allow deleting any landing zone
# NOTE: Is allowed if project is archived
rules.add_perm(
    'landingzones.delete_zone_all',
    pr_rules.is_project_owner | pr_rules.is_project_delegate,
)
