#class_name = EntityOrganisation
#table_name = tbl_entity_organisation
#prefix =PRE
#postfix =POST
#columns_to_create = [id, entity_id, entity_organisation_type_id, organisation_id, intermediary_id, currency_id, start_date, end_date, mail_option_id] #id - primary_key autoincrement=True
#cont_name = entity
#html_template_name = generic
#dbsession = DBSession
#controller_name = EntityController
#view_cols_list = [entity_id, entity_organisation_type_id, organisation_id, intermediary_id, currency_id, start_date, end_date, mail_option_id]
#search_cols_list = [entity_id, entity_organisation_type_id, organisation_id, intermediary_id, currency_id, start_date, end_date, mail_option_id]
#pdf_cols_list = [entity_id, entity_organisation_type_id, organisation_id, intermediary_id, currency_id, start_date, end_date, mail_option_id]
#link_to_id_or_None = None
#link_class_name_None = None
"""
@q: 1ggf=wv$h"ay 2ggf=wv$h"by 3ggf=wv$h"cy 4ggf=wv$h"dy 5ggf[wvt]"ey 6ggf=wv$h"fy 7ggf=wv$h"gy 8ggf=wv$h"hy 9ggf=wv$h"iy 10ggf[wvt]"jy 11ggf[wvt]"ky 12ggf[wvt]"ly
@w: "api "bgpi "cgp i "dgp i "egpi "fgp i "ggp i "hgp i "igp i "jpi "kpi "lpi
@t: 23ggVGd22ggo_tgcreateclas
@r: 16ggf: wv$"qy 17ggf: wv$"wy 18ggf: wv$"ty @q@t
Instructions: run @r then complete the snip with <ctr-l> then <escape> then @w
"""
##################################################################################################################
#class_name = EntityOrganisation
#table_name =tbl_entity_organisation
#prefix =PRE
#postfix =POST
#columns_to_create = [id, entity_id, entity_organisation_type_id, organisation_id, intermediary_id, currency_id, start_date, end_date, mail_option_id] #id - primary_key autoincrement=True
#cont_name =entity
#html_template_name =generic
#dbsession =DBSession
#controller_name =EntityController
#view_cols_list = [entity_id, entity_organisation_type_id, organisation_id, intermediary_id, currency_id, start_date, end_date, mail_option_id]
#search_cols_list = [entity_id, entity_organisation_type_id, organisation_id, intermediary_id, currency_id, start_date, end_date, mail_option_id]
#pdf_cols_list = [entity_id, entity_organisation_type_id, organisation_id, intermediary_id, currency_id, start_date, end_date, mail_option_id]
#link_to_id_or_None =
#link_class_name_None =

############################
# Model
############################

class EntityOrganisation(DeclarativeBase):
    __tablename__='tbl_entity_organisation'
    id = Column(Integer, autoincrement=True, primary_key=True)
    entity_id = Column(Unicode(255))
    entity_organisation_type_id = Column(Unicode(255))
    organisation_id = Column(Unicode(255))
    intermediary_id = Column(Unicode(255))
    currency_id = Column(Unicode(255))
    start_date = Column(Unicode(255))
    end_date = Column(Unicode(255))
    mail_option_id = Column(Unicode(255))

    active = Column(Boolean, default=True)
    added_by = Column(Integer, nullable=False)
    added = Column(DateTime, default=datetime.now)

############################
# Controller
############################


class EntityController(BaseController):
    """Docstring for entity."""

    def __init__(self, *args, **kwargs):
        pass

    @require(predicates.not_anonymous())
    @expose('rocket_app.templates.generic')
    def tbl_entity_organisations(self, *args, **kwargs):
        html = self.get_active_tbl_entity_organisation_html(*args, **kwargs)
        javascript = self.get_javascript_tbl_entity_organisation_onload()
        title = "Tbl_entity_organisation"
        return dict(title=title, html=html, javascript=javascript)

    @expose()
    def get_active_tbl_entity_organisation_html(self, *args, **kwargs):
        usernow = request.identity['user']
        dbase_query = self.get_active_tbl_entity_organisation_list(*args, **kwargs)
        outputlist = []
        for item in dbase_query:
            outputlist.append({
                'entity_id' : "<div class='edit tbl_entity_organisation_edit' tbl_entity_organisation_id='{1}'>{0}</div>".format(item.entity_id, item.id),
                'entity_organisation_type_id' : item.entity_organisation_type_id,
                'organisation_id' : item.organisation_id,
                'intermediary_id' : item.intermediary_id,
                'currency_id' : item.currency_id,
                'start_date' : item.start_date,
                'end_date' : item.end_date,
                'mail_option_id' : item.mail_option_id,
                             })
        dbcolumnlist=[
                'entity_id',
                'entity_organisation_type_id',
                'organisation_id',
                'intermediary_id',
                'currency_id',
                'start_date',
                'end_date',
                'mail_option_id',
                    ]
        theadlist=[
                'Entity_Id',
                ' Entity_Organisation_Type_Id',
                ' Organisation_Id',
                ' Intermediary_Id',
                ' Currency_Id',
                ' Start_Date',
                ' End_Date',
                ' Mail_Option_Id',
                ]
        tbl_entity_organisationtable = build_html_table(outputlist, dbcolumnlist, theadlist, "tbl_entity_organisation_table")
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-6">
                            <h4 class="card-title">Tbl_entity_organisation</h4>
                        </div>
                        <div class="col-md-6 text-right">
                            <button id="create_new_tbl_entity_organisation" class="btn btn-primary ml-auto">Create a new Tbl_entity_organisation</button>
                        </div>
                    </div>
                    <div class="row d-flex align-items-center">
                        <div class="col-md-4">
                            <input type="text" class="form-control search" name="searchphrase" placeholder="Search">
                        </div>
                        <div class="col-md-8">
                            <button class="btn btn-primary action_search">Search</button>
                            <button class="btn btn-primary">Reset</button>
                        </div>
                    </div>
                    <hr>
                </div>
                <div class="card-body">
                    <div class="table-responsive">
                        {tbl_entity_organisationtable}
                    </div>
                </div>
                </div>
            </div>
            <div id='dialogdiv'></div>
        """
        return html

    @expose()
    def get_javascript_tbl_entity_organisation_onload(self, *args, **kwargs):
        javascript = """
        $("#create_new_tbl_entity_organisation").click(function(){
            $('#dialogdiv').load('/entity/get_modal_new_tbl_entity_organisation?', function(data){
                return false;
            });
        });
        $(".tbl_entity_organisation_edit").click(function(){
            var kwargs = 'tbl_entity_organisation_id='+$(this).attr('tbl_entity_organisation_id');
            $('#dialogdiv').load('/entity/get_modal_edit_tbl_entity_organisation?'+kwargs, function(data){
                return false;
            });
        });
        """
        return javascript

    @expose()
    def get_modal_new_tbl_entity_organisation(self, *args, **kwargs):
        html = """
        <div class="modal fade" id="dialog_new_tbl_entity_organisation" tabindex="-1" role="dialog" aria-labelledby="mytbl_entity_organisationLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-6">
                            <h4 class="card-title">New Tbl_entity_organisation</h4>
                        </div>
                    </div>
                    <div class="modal-body">
                        <form id='form_new_tbl_entity_organisation'>
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="entity_id">Entity_Id</label>
						<div class="col-md-9">
							<input id="entity_id" type="text" name="entity_id" class="form-control" required='true'>
						</div>
					</div>
				</div>
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="entity_organisation_type_id"> Entity_Organisation_Type_Id</label>
						<div class="col-md-9">
							<input id="entity_organisation_type_id" type="text" name="entity_organisation_type_id" class="form-control" required='true'>
						</div>
					</div>
				</div>
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="organisation_id"> Organisation_Id</label>
						<div class="col-md-9">
							<input id="organisation_id" type="text" name="organisation_id" class="form-control" required='true'>
						</div>
					</div>
				</div>
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="intermediary_id"> Intermediary_Id</label>
						<div class="col-md-9">
							<input id="intermediary_id" type="text" name="intermediary_id" class="form-control" required='true'>
						</div>
					</div>
				</div>
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="currency_id"> Currency_Id</label>
						<div class="col-md-9">
							<input id="currency_id" type="text" name="currency_id" class="form-control" required='true'>
						</div>
					</div>
				</div>
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="start_date"> Start_Date</label>
						<div class="col-md-9">
							<input id="start_date" type="text" name="start_date" class="form-control" required='true'>
						</div>
					</div>
				</div>
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="end_date"> End_Date</label>
						<div class="col-md-9">
							<input id="end_date" type="text" name="end_date" class="form-control" required='true'>
						</div>
					</div>
				</div>
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="mail_option_id"> Mail_Option_Id</label>
						<div class="col-md-9">
							<input id="mail_option_id" type="text" name="mail_option_id" class="form-control" required='true'>
						</div>
					</div>
				</div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button id='save_new_tbl_entity_organisation' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary tbl_entity_organisation_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
        setFormValidation('#form_new_tbl_entity_organisation');
        $("#start_date").datetimepicker({ format: 'DD/MM/YYYY' });
        $("#end_date").datetimepicker({ format: 'DD/MM/YYYY' });
        $('#save_new_tbl_entity_organisation').click(function(){
             var valid = FormIsValid("#form_new_tbl_entity_organisation");
             if(valid){
                var formserial = getFormData('#form_new_tbl_entity_organisation');
                var data = {data : JSON.stringify(formserial)};

                $.post('/entity/save_new_tbl_entity_organisation?', data, function(data){
                    var result = JSON.parse(data);
                    if(result.success === true){
                        $.redirect('/entity/tbl_entity_organisations');
                    };
                    return false;
                });
             }
        });
        $('.tbl_entity_organisation_back').click(function(){
            $('#dialog_new_tbl_entity_organisation').modal('hide');
        });
        $('#dialog_new_tbl_entity_organisation').modal();
        </script>
     	"""
        return html + javascript

    @expose()
    def get_modal_edit_tbl_entity_organisation(self, *args, **kwargs):
        tbl_entity_organisation_id = kwargs.get('tbl_entity_organisation_id', None)
        if not tbl_entity_organisation_id: return ''
        this = self.get_tbl_entity_organisation_by_id(*args, **kwargs)
        if not this: return ''
        checked = 'checked' if this.active else ''
        html = f"""
        <div class="modal fade" id="dialog_edit_tbl_entity_organisation" tabindex="-1" role="dialog" aria-labelledby="mytbl_entity_organisationLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-6">
                            <h4 class="card-title">New Tbl_entity_organisation</h4>
                        </div>
                    </div>
                    <div class="modal-body">
                        <form id='form_edit_tbl_entity_organisation'>
                            <div style='display: none' class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="tbl_entity_organisation_id">Id</label>
						<div class="col-md-9">
							<input id="id" type="text" name="tbl_entity_organisation_id" value="{this.id}" class="form-control" required='true'>
						</div>
					</div>
				</div>
                            <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="entity_id"> Entity_Id</label>
						<div class="col-md-9">
							<input id="entity_id" type="text" name="entity_id" value="{this.entity_id}" class="form-control" required='true'>
						</div>
					</div>
				</div>
                            <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="entity_organisation_type_id"> Entity_Organisation_Type_Id</label>
						<div class="col-md-9">
							<input id="entity_organisation_type_id" type="text" name="entity_organisation_type_id" value="{this.entity_organisation_type_id}" class="form-control" required='true'>
						</div>
					</div>
				</div>
                            <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="organisation_id"> Organisation_Id</label>
						<div class="col-md-9">
							<input id="organisation_id" type="text" name="organisation_id" value="{this.organisation_id}" class="form-control" required='true'>
						</div>
					</div>
				</div>
                            <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="intermediary_id"> Intermediary_Id</label>
						<div class="col-md-9">
							<input id="intermediary_id" type="text" name="intermediary_id" value="{this.intermediary_id}" class="form-control" required='true'>
						</div>
					</div>
				</div>
                            <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="currency_id"> Currency_Id</label>
						<div class="col-md-9">
							<input id="currency_id" type="text" name="currency_id" value="{this.currency_id}" class="form-control" required='true'>
						</div>
					</div>
				</div>
                            <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="start_date"> Start_Date</label>
						<div class="col-md-9">
							<input id="start_date" type="text" name="start_date" value="{this.start_date}" class="form-control" required='true'>
						</div>
					</div>
				</div>
                            <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="end_date"> End_Date</label>
						<div class="col-md-9">
							<input id="end_date" type="text" name="end_date" value="{this.end_date}" class="form-control" required='true'>
						</div>
					</div>
				</div>
                            <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="mail_option_id"> Mail_Option_Id</label>
						<div class="col-md-9">
							<input id="mail_option_id" type="text" name="mail_option_id" value="{this.mail_option_id}" class="form-control" required='true'>
						</div>
					</div>
				</div>
                            <div class="form-group row">
                              <label class="col-4 col-form-label" for="active" required>Active</label>
                              <div class="col-8"><div class="form-check">
                                <input class="form-check-input" type="checkbox" name="active" id="active" {checked}/></div>
                              </div>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button id='save_edit_tbl_entity_organisation' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary tbl_entity_organisation_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
        setFormValidation('#form_edit_tbl_entity_organisation');
        $("#start_date").datetimepicker({ format: 'DD/MM/YYYY' });
        $("#end_date").datetimepicker({ format: 'DD/MM/YYYY' });
        $('#save_edit_tbl_entity_organisation').click(function(){
             var valid = FormIsValid("#form_edit_tbl_entity_organisation");
             if(valid){
                var formserial = getFormData('#form_edit_tbl_entity_organisation');
                var data = {data : JSON.stringify(formserial)};

                $.post('/entity/save_edit_tbl_entity_organisation?', data, function(data){
                    var result = JSON.parse(data);
                    if(result.success === true){
                        $.redirect('/entity/tbl_entity_organisations');
                    };
                    return false;
                });
             }
        });
        $('.tbl_entity_organisation_back').click(function(){
            $('#dialog_edit_tbl_entity_organisation').modal('hide');
        });
        $('#dialog_edit_tbl_entity_organisation').modal();
        </script>
     	"""
        return html + javascript

    @expose()
    def save_new_tbl_entity_organisation(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        if not data: return json.dumps({'success' : False, 'data' : 'No data provided'})
        usernow = request.identity['user']
        this = EntityOrganisation()
        this.entity_id = data.get('entity_id', None)
        this.entity_organisation_type_id = data.get('entity_organisation_type_id', None)
        this.organisation_id = data.get('organisation_id', None)
        this.intermediary_id = data.get('intermediary_id', None)
        this.currency_id = data.get('currency_id', None)
        this.start_date = data.get('start_date', None)
        this.end_date = data.get('end_date', None)
        this.mail_option_id = data.get('mail_option_id', None)
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()
        return json.dumps({'success' : True, 'data' : this.id})

    @expose()
    def save_edit_tbl_entity_organisation(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        if not data: return json.dumps({'success' : False, 'data' : 'No data provided'})
        usernow = request.identity['user']
        this = self.get_tbl_entity_organisation_by_id(**data)
        if not this: return json.dumps({'success' : False, 'data' : 'No tbl_entity_organisation found for id provided'})
        this.entity_id = data.get('entity_id', None)
        this.entity_organisation_type_id = data.get('entity_organisation_type_id', None)
        this.organisation_id = data.get('organisation_id', None)
        this.intermediary_id = data.get('intermediary_id', None)
        this.currency_id = data.get('currency_id', None)
        this.start_date = data.get('start_date', None)
        this.end_date = data.get('end_date', None)
        this.mail_option_id = data.get('mail_option_id', None)
        if not data.get('active', None): this.active = False
        DBSession.flush()
        return json.dumps({'success' : True, 'data' : this.id})

    @expose()
    def get_tbl_entity_organisation_by_id(self, *args, **kwargs):
        return DBSession.query(EntityOrganisation). \
            filter(EntityOrganisation.id==kwargs.get('tbl_entity_organisation_id', None)). \
            first()

    @expose()
    def get_active_tbl_entity_organisation_list(self, *args, **kwargs):
        searchphrase = kwargs.get('searchphrase', None)

        tbl_entity_organisation_entity_id = kwargs.get('tbl_entity_organisation_entity_id', None)
        tbl_entity_organisation_entity_organisation_type_id = kwargs.get('tbl_entity_organisation_entity_organisation_type_id', None)
        tbl_entity_organisation_organisation_id = kwargs.get('tbl_entity_organisation_organisation_id', None)
        tbl_entity_organisation_intermediary_id = kwargs.get('tbl_entity_organisation_intermediary_id', None)
        tbl_entity_organisation_currency_id = kwargs.get('tbl_entity_organisation_currency_id', None)
        start_date_start = kwargs.get('start_date_start', None)
        start_date_end = kwargs.get('start_date_end', None)
        end_date_start = kwargs.get('end_date_start', None)
        end_date_end = kwargs.get('end_date_end', None)
        tbl_entity_organisation_mail_option_id = kwargs.get('tbl_entity_organisation_mail_option_id', None)

        if tbl_entity_organisation_entity_id:
            dbase_query = DBSession.query(EntityOrganisation). \
		    filter(EntityOrganisation.tbl_entity_organisation_entity_id==tbl_entity_organisation_entity_id). \
                        filter(EntityOrganisation.active==1). \
		    order_by(asc(EntityOrganisation.tbl_entity_organisation_id)).limit(LIMIT)
        if tbl_entity_organisation_entity_organisation_type_id:
            dbase_query = DBSession.query(EntityOrganisation). \
		    filter(EntityOrganisation.tbl_entity_organisation_entity_organisation_type_id==tbl_entity_organisation_entity_organisation_type_id). \
                        filter(EntityOrganisation.active==1). \
		    order_by(asc(EntityOrganisation.tbl_entity_organisation_id)).limit(LIMIT)
        if tbl_entity_organisation_organisation_id:
            dbase_query = DBSession.query(EntityOrganisation). \
		    filter(EntityOrganisation.tbl_entity_organisation_organisation_id==tbl_entity_organisation_organisation_id). \
                        filter(EntityOrganisation.active==1). \
		    order_by(asc(EntityOrganisation.tbl_entity_organisation_id)).limit(LIMIT)
        if tbl_entity_organisation_intermediary_id:
            dbase_query = DBSession.query(EntityOrganisation). \
		    filter(EntityOrganisation.tbl_entity_organisation_intermediary_id==tbl_entity_organisation_intermediary_id). \
                        filter(EntityOrganisation.active==1). \
		    order_by(asc(EntityOrganisation.tbl_entity_organisation_id)).limit(LIMIT)
        if tbl_entity_organisation_currency_id:
            dbase_query = DBSession.query(EntityOrganisation). \
		    filter(EntityOrganisation.tbl_entity_organisation_currency_id==tbl_entity_organisation_currency_id). \
                        filter(EntityOrganisation.active==1). \
		    order_by(asc(EntityOrganisation.tbl_entity_organisation_id)).limit(LIMIT)
        if start_date_start:
            if not start_date_end: start_date_end = datetime.date(datetime.now())
            dbase_query = DBSession.query(EntityOrganisation). \
			filter(EntityOrganisation.start_date>=start_date_start). \
			filter(EntityOrganisation.start_date<=start_date_end). \
                        filter(EntityOrganisation.active==1). \
			order_by(asc(EntityOrganisation.id)).limit(LIMIT)
        if end_date_start:
            if not end_date_end: end_date_end = datetime.date(datetime.now())
            dbase_query = DBSession.query(EntityOrganisation). \
			filter(EntityOrganisation.end_date>=end_date_start). \
			filter(EntityOrganisation.end_date<=end_date_end). \
                        filter(EntityOrganisation.active==1). \
			order_by(asc(EntityOrganisation.id)).limit(LIMIT)
        if tbl_entity_organisation_mail_option_id:
            dbase_query = DBSession.query(EntityOrganisation). \
		    filter(EntityOrganisation.tbl_entity_organisation_mail_option_id==tbl_entity_organisation_mail_option_id). \
                        filter(EntityOrganisation.active==1). \
		    order_by(asc(EntityOrganisation.tbl_entity_organisation_id)).limit(LIMIT)
        else:
            dbase_query = DBSession.query(EntityOrganisation). \
                filter(EntityOrganisation.active==1). \
                order_by(asc(EntityOrganisation.id)). \
                limit(LIMIT)
        return dbase_query
