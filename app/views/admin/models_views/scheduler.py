from datetime import datetime

from flask import url_for, flash, request
from flask_admin import BaseView, expose
from werkzeug.utils import redirect

from app.helpers.data import save_to_db
from ....helpers.data_getter import DataGetter

class SchedulerView(BaseView):

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('admin.login_view', next=request.url))
        event = DataGetter.get_event(kwargs['event_id'])
        if not event.has_session_speakers:
            return self.render('/gentelella/admin/event/info/enable_module.html', active_page='scheduler', title='Scheduler', event=event)

    @expose('/')
    def display_view(self, event_id):
        sessions = DataGetter.get_sessions_by_event_id(event_id)
        event = DataGetter.get_event(event_id)
        return self.render('/gentelella/admin/event/scheduler/scheduler.html', sessions=sessions, event=event)

    @expose('/publish')
    def publish(self, event_id):
        event = DataGetter.get_event(event_id)
        event.schedule_published_on = datetime.now()
        save_to_db(event, "Event schedule published")
        flash('The schedule has been published for this event', 'success')
        return redirect(url_for('.display_view', event_id=event_id))

    @expose('/unpublish')
    def unpublish(self, event_id):
        event = DataGetter.get_event(event_id)
        event.schedule_published_on = None
        save_to_db(event, "Event schedule unpublished")
        flash('The schedule has been unpublished for this event', 'success')
        return redirect(url_for('.display_view', event_id=event_id))
