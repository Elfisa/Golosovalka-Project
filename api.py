from flask import jsonify
from db_data import db_session
from main import blueprint
from db_data.__all_models import Vote


@blueprint.route('/api/newvotes')
def get_new_votes():
    db_sess = db_session.create_session()
    golosovalki = db_sess.query(Vote).all()
    return jsonify(
        {
            'vote':
                [item.to_dict(only=('id', 'groups[0].id'))
                 for item in golosovalki]
        }
    )
