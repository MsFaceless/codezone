#class_name = Entity
#table_name = tbl_entity
#prefix =PRE
#postfix =POST
#columns_to_create = [id, entity_type_id, code, register_date] #id - primary_key autoincrement=True
#cont_name = entity
#html_template_name = generic
#dbsession = DBSession
#controller_name = EntityController
#view_cols_list = [entity_type_id, code, register_date]
#search_cols_list = [entity_type_id, code, register_date]
#pdf_cols_list = [entity_type_id, code, register_date]
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
#class_name = Entity
#table_name =tbl_entity
#prefix =PRE
#postfix =POST
#columns_to_create = [id, entity_type_id, code, register_date] #id - primary_key autoincrement=True
#cont_name =entity
#html_template_name =generic
#dbsession =DBSession
#controller_name =EntityController
#view_cols_list = [entity_type_id, code, register_date]
#search_cols_list = [entity_type_id, code, register_date]
#pdf_cols_list = [entity_type_id, code, register_date]
#link_to_id_or_None =
#link_class_name_None =

############################
# Model
############################

class Entity(DeclarativeBase):
    __tablename__='tbl_entity'
    id = Column(Integer, autoincrement=True, primary_key=True)
    entity_type_id = Column(Unicode(255))
    code = Column(Unicode(255))
    register_date = Column(Unicode(255))

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
    def tbl_entitys(self, *args, **kwargs):
        html = self.get_active_tbl_entity_html(*args, **kwargs)
        javascript = self.get_javascript_tbl_entity_onload()
        title = "Tbl_entity"
        return dict(title=title, html=html, javascript=javascript)

    @expose()
    def get_active_tbl_entity_html(self, *args, **kwargs):
        usernow = request.identity['user']
        dbase_query = self.get_active_tbl_entity_list(*args, **kwargs)
        outputlist = []
        for item in dbase_query:
            outputlist.append({
                'entity_type_id' : "<div class='edit tbl_entity_edit' tbl_entity_id='{1}'>{0}</div>".format(item.entity_type_id, item.id),
                'code' : item.code,
                'register_date' : item.register_date,
                             })
        dbcolumnlist=[
                'entity_type_id',
                'code',
                'register_date',
                    ]
        theadlist=[
                'Entity_Type_Id',
                'Code',
                'Register_Date',
                ]
        tbl_entitytable = build_html_table(outputlist, dbcolumnlist, theadlist, "tbl_entity_table")
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-6">
                            <h4 class="card-title">Tbl_entity</h4>
                        </div>
                        <div class="col-md-6 text-right">
                            <button id="create_new_tbl_entity" class="btn btn-primary ml-auto">Create a new Tbl_entity</button>
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
                        {tbl_entitytable}
                    </div>
                </div>
                </div>
            </div>
            <div id='dialogdiv'></div>
        """
        return html

    @expose()
    def get_javascript_tbl_entity_onload(self, *args, **kwargs):
        javascript = """
        $("#create_new_tbl_entity").click(function(){
            $('#dialogdiv').load('/entity/get_modal_new_tbl_entity?', function(data){
                return false;
            });
        });
        $(".tbl_entity_edit").click(function(){
            var kwargs = 'tbl_entity_id='+$(this).attr('tbl_entity_id');
            $('#dialogdiv').load('/entity/get_modal_edit_tbl_entity?'+kwargs, function(data){
                return false;
            });
        });
        """
        return javascript

    @expose()
    def get_modal_new_tbl_entity(self, *args, **kwargs):
        html = """
        <div class="modal fade" id="dialog_new_tbl_entity" tabindex="-1" role="dialog" aria-labelledby="mytbl_entityLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-6">
                            <h4 class="card-title">New Tbl_entity</h4>
                        </div>
                    </div>
                    <div class="modal-body">
                        <form id='form_new_tbl_entity'>
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="entity_type_id">Entity_Type_Id</label>
						<div class="col-md-9">
							<input id="entity_type_id" type="text" name="entity_type_id" class="form-control" required='true'>
						</div>
					</div>
				</div>
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="code">Code</label>
						<div class="col-md-9">
							<input id="code" type="text" name="code" class="form-control" required='true'>
						</div>
					</div>
				</div>
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="register_date">Register_Date</label>
						<div class="col-md-9">
							<input id="register_date" type="text" name="register_date" class="form-control" required='true'>
						</div>
					</div>
				</div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button id='save_new_tbl_entity' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary tbl_entity_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
        setFormValidation('#form_new_tbl_entity');
        $("#register_date").datetimepicker({ format: 'DD/MM/YYYY' });
        $('#save_new_tbl_entity').click(function(){
             var valid = FormIsValid("#form_new_tbl_entity");
             if(valid){
                var formserial = getFormData('#form_new_tbl_entity');
                var data = {data : JSON.stringify(formserial)};

                $.post('/entity/save_new_tbl_entity?', data, function(data){
                    var result = JSON.parse(data);
                    if(result.success === true){
                        $.redirect('/entity/tbl_entitys');
                    };
                    return false;
                });
             }
        });
        $('.tbl_entity_back').click(function(){
            $('#dialog_new_tbl_entity').modal('hide');
        });
        $('#dialog_new_tbl_entity').modal();
        </script>
     	"""
        return html + javascript

    @expose()
    def get_modal_edit_tbl_entity(self, *args, **kwargs):
        tbl_entity_id = kwargs.get('tbl_entity_id', None)
        if not tbl_entity_id: return ''
        this = self.get_tbl_entity_by_id(*args, **kwargs)
        if not this: return ''
        checked = 'checked' if this.active else ''
        html = f"""
        <div class="modal fade" id="dialog_edit_tbl_entity" tabindex="-1" role="dialog" aria-labelledby="mytbl_entityLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-6">
                            <h4 class="card-title">New Tbl_entity</h4>
                        </div>
                    </div>
                    <div class="modal-body">
                        <form id='form_edit_tbl_entity'>
                            <div style='display: none' class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="tbl_entity_id">Id</label>
						<div class="col-md-9">
							<input id="id" type="text" name="tbl_entity_id" value="{this.id}" class="form-control" required='true'>
						</div>
					</div>
				</div>
                            <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="entity_type_id">Entity_Type_Id</label>
						<div class="col-md-9">
							<input id="entity_type_id" type="text" name="entity_type_id" value="{this.entity_type_id}" class="form-control" required='true'>
						</div>
					</div>
				</div>
                            <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="code">Code</label>
						<div class="col-md-9">
							<input id="code" type="text" name="code" value="{this.code}" class="form-control" required='true'>
						</div>
					</div>
				</div>
                            <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="register_date">Register_Date</label>
						<div class="col-md-9">
							<input id="register_date" type="text" name="register_date" value="{this.register_date}" class="form-control" required='true'>
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
                        <button id='save_edit_tbl_entity' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary tbl_entity_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
        setFormValidation('#form_edit_tbl_entity');
        $("#register_date").datetimepicker({ format: 'DD/MM/YYYY' });
        $('#save_edit_tbl_entity').click(function(){
             var valid = FormIsValid("#form_edit_tbl_entity");
             if(valid){
                var formserial = getFormData('#form_edit_tbl_entity');
                var data = {data : JSON.stringify(formserial)};

                $.post('/entity/save_edit_tbl_entity?', data, function(data){
                    var result = JSON.parse(data);
                    if(result.success === true){
                        $.redirect('/entity/tbl_entitys');
                    };
                    return false;
                });
             }
        });
        $('.tbl_entity_back').click(function(){
            $('#dialog_edit_tbl_entity').modal('hide');
        });
        $('#dialog_edit_tbl_entity').modal();
        </script>
     	"""
        return html + javascript

    @expose()
    def save_new_tbl_entity(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        if not data: return json.dumps({'success' : False, 'data' : 'No data provided'})
        usernow = request.identity['user']
        this = Entity()
        this.entity_type_id = data.get('entity_type_id', None)
        this.code = data.get('code', None)
        this.register_date = data.get('register_date', None)
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()
        return json.dumps({'success' : True, 'data' : this.id})

    @expose()
    def save_edit_tbl_entity(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        if not data: return json.dumps({'success' : False, 'data' : 'No data provided'})
        usernow = request.identity['user']
        this = self.get_tbl_entity_by_id(**data)
        if not this: return json.dumps({'success' : False, 'data' : 'No tbl_entity found for id provided'})
        this.entity_type_id = data.get('entity_type_id', None)
        this.code = data.get('code', None)
        this.register_date = data.get('register_date', None)
        if not data.get('active', None): this.active = False
        DBSession.flush()
        return json.dumps({'success' : True, 'data' : this.id})

    @expose()
    def get_tbl_entity_by_id(self, *args, **kwargs):
        return DBSession.query(Entity). \
            filter(Entity.id==kwargs.get('tbl_entity_id', None)). \
            first()

    @expose()
    def get_active_tbl_entity_list(self, *args, **kwargs):
        searchphrase = kwargs.get('searchphrase', None)

        tbl_entity_entity_type_id = kwargs.get('tbl_entity_entity_type_id', None)
        code = kwargs.get('code', None)
        register_date_start = kwargs.get('register_date_start', None)
        register_date_end = kwargs.get('register_date_end', None)

        if tbl_entity_entity_type_id:
            dbase_query = DBSession.query(Entity). \
		    filter(Entity.tbl_entity_entity_type_id==tbl_entity_entity_type_id). \
                        filter(Entity.active==1). \
		    order_by(asc(Entity.tbl_entity_id)).limit(LIMIT)
        if code:
            searchphrase = "%"+kwargs['code']+"%"
            dbase_query = DBSession.query(Entity). \
			filter(Entity.code.like(searchphrase)). \
                        filter(Entity.active==1). \
			order_by(asc(Entity.code)).limit(LIMIT)
        if register_date_start:
            if not register_date_end: register_date_end = datetime.date(datetime.now())
            dbase_query = DBSession.query(Entity). \
			filter(Entity.register_date>=register_date_start). \
			filter(Entity.register_date<=register_date_end). \
                        filter(Entity.active==1). \
			order_by(asc(Entity.id)).limit(LIMIT)
        else:
            dbase_query = DBSession.query(Entity). \
                filter(Entity.active==1). \
                order_by(asc(Entity.id)). \
                limit(LIMIT)
        return dbase_query
