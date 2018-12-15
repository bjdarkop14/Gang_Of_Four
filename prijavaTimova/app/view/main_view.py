from flask import Blueprint, request, jsonify

from ..controller.main_controller import create_user, auth_user, get_all_areas, get_my_groups

user = Blueprint('user', __name__, url_prefix='/api/user')
areas = Blueprint('areas', __name__, url_prefix='/api/areas')
group = Blueprint('group', __name__, url_prefix='/api/group')


@user.route('/signup', methods=['POST'])
def user_signup():
    if request.method == 'POST':  # sign up
        body = request.json
        user = create_user(body)

        return jsonify(user.to_dict()), 200


@user.route('/login', methods=['POST'])
def user_login():
    if request.method == 'POST':  # log in
        body = request.json
        user = auth_user(body)

        if user == -1:
            return jsonify({'error': 'wrong password or username'}), 400
        return jsonify(user.to_dict()), 201

@areas.route('/', methods=['GET'])
def view_areas():
    if request.method == 'GET':  # log in
        areas = get_all_areas()

        return jsonify([area.to_dict() for area in areas]), 201

# @group.route('/', methods=['GET'])
# def view_groups():
#     if request.method == 'GET':  # sign up
#         body = request.json
#         my_groups = get_my_groups(body)
#
#         return jsonify([group.to_dict() for group in my_groups]), 201
#

# @teams.route('/', methods=['GET', 'POST'])
# def teams_view():
#     if request.method == 'GET':  # get all teams
#         all_teams = get_all_teams()
#
#         response_body = [t.to_dict() for t in all_teams]
#         return jsonify(response_body), 200
#
#     if request.method == 'POST':  # create a new team
#         # mention validation issues
#         body = request.json
#         created = create_team(body)
#         if created == -1:
#             return jsonify({'error': 'team field blank'}), 400
#         elif isinstance(created, tuple):
#             if created[0] == 2:
#                 return jsonify({'error': 'team member number {} lacks field'.format(created[1])}), 400
#             elif created[0] == 3:
#                 return jsonify({'error': 'wrong team count {}'.format(created[1])}), 400
#         return jsonify(created), 201
#
#
# @teams.route('/<string:team_uuid>', methods=['GET', 'PUT', 'DELETE'])
# def single_team_view(team_uuid):
#     if request.method == 'GET':  # get the team
#         team = get_team(team_uuid)
#         if team is None:
#             return jsonify({'error': 'team with unique id {} not found'.format(team_uuid)}), 404
#
#         response_body = team.to_dict()
#         return jsonify(response_body), 200
#
#     if request.method == 'PUT':  # update the team
#         body = request.json
#         updated = update_team(body, team_uuid)
#         if updated is None:
#             return jsonify({'error': 'team with unique id {} not found'.format(team_uuid)}), 404
#         if updated == -1:
#             return jsonify({'error': 'team field blank'}), 400
#         elif isinstance(updated, tuple):
#             if updated[0] == 2:
#                 return jsonify({'error': 'team member number {} lacks field'.format(updated[1])}), 400
#             elif updated[0] == 3:
#                 return jsonify({'error': 'wrong team count {}'.format(updated[1])}), 400
#
#         return jsonify(updated), 200
#
#     if request.method == 'DELETE':  # remove the team
#         success = delete_team(team_uuid)
#
#         if not success:
#             return jsonify({'error': 'team with unique id {} not found'.format(team_uuid)}), 404
#
#         return jsonify({}), 204
#
#
# @members.route('/<string:team_member_id>', methods=['GET', 'PUT', 'DELETE'])
# def single_team_member_view(team_member_id):
#     if request.method == 'GET':  # get the team member
#         team_member = get_team_member(team_member_id)
#         if team_member is None:
#             return jsonify({'error': 'team member with unique id {} not found'.format(team_member_id)}), 404
#
#         response_body = team_member.to_dict()
#         return jsonify(response_body), 200
#
#     if request.method == 'PUT':  # update the team member
#         body = request.json
#         updated = update_team_member(body, team_member_id)
#         if updated is None:
#             return jsonify({'error': 'team member with unique id {} not found'.format(team_member_id)}), 404
#         if updated == 2:
#             return jsonify({'error': 'team member field blank'}), 400
#
#         return jsonify(updated), 200
#
#     if request.method == 'DELETE':  # remove the team member
#         success = delete_team_member(team_member_id)
#
#         if success == 2:
#             return jsonify({'error': 'members too low'}), 400
#         elif not success:
#             return jsonify({'error': 'team member with unique id {} not found'.format(team_member_id)}), 404
#
#         return jsonify({}), 204
