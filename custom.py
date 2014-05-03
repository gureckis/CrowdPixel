# this file imports custom routes into the experiment server

from flask import Blueprint, render_template, request, jsonify, Response, abort, current_app
from jinja2 import TemplateNotFound
from functools import wraps
from sqlalchemy import or_, Column, Integer, String, DateTime, Boolean, Float, Text

from psiturk.psiturk_config import PsiturkConfig
from psiturk.experiment_errors import ExperimentError
from psiturk.user_utils import PsiTurkAuthorization, nocache

# # Database setup
from psiturk.db import db_session, init_db, Base
from psiturk.models import Participant
from json import dumps, loads

from random import shuffle
from custom_models import Pixels

# load the configuration options
config = PsiturkConfig()
config.load_config()
myauth = PsiTurkAuthorization(config)  # if you want to add a password protect route use this

# explore the Blueprint
custom_code = Blueprint('custom_code', __name__, template_folder='templates', static_folder='static')


###########################################################
#  serving warm, fresh, & sweet custom, user-provided routes
#  add them here
###########################################################

#----------------------------------------------
# example accessing data
#----------------------------------------------
@custom_code.route('/get_condition')
def getcondition():
	#save the tiles to the 
	try:
		pix = Pixels.query.order_by(Pixels.n_completed.asc()).first()
	except:
		current_app.logger.info("no pixels in the database.  you may need to run setup.py first")
		abort(404)
	else:
		condition = {"filename": pix.filename, "width": pix.width, "height": pix.height}
		return jsonify(condition=condition)

@custom_code.route('/complete_condition', methods=['POST'])
def complete_condition():
	if not 'filename' in request.form:
		abort(404)
	else:
		try:
			pix = Pixels.query.filter(Pixels.filename==request.form['filename']).one()
			pix.n_completed = pix.n_completed + 1
			if pix.illustrations == None:
				pix.illustrations = request.form['drawing_data']
			else:
				pix.illustrations = pix.illustrations + request.form['drawing_data']
			db_session.add(pix)
			db_session.commit()
		except:
			current_app.logger.info("error saving")
			abort(404)
		else:
			return jsonify(status="saved")


