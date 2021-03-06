#class_name = Insurer
#table_name = tbl_insurer
#prefix =PRE
#postfix =POST
#columns_to_create = [id, entity_organisation_id] #id - primary_key autoincrement=True
#cont_name = entity
#html_template_name = generic
#dbsession = DBSession
#controller_name = EntityController
#view_cols_list = [entity_organisation_id]
#search_cols_list = [entity_organisation_id]
#pdf_cols_list = [entity_organisation_id]
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
#class_name = Insurer
#table_name =tbl_insurer
#prefix =PRE
#postfix =POST
#columns_to_create = [id, entity_organisation_id] #id - primary_key autoincrement=True
#cont_name =entity
#html_template_name =generic
#dbsession =DBSession
#controller_name =EntityController
#view_cols_list = [entity_organisation_id]
#search_cols_list = [entity_organisation_id]
#pdf_cols_list = [entity_organisation_id]
#link_to_id_or_None =
#link_class_name_None =

############################
# Controller
############################


class EntityController(BaseController):
    """Docstring for entity."""

    def __init__(self, *args, **kwargs):
        pass

    @require(predicates.not_anonymous())
    @expose('rocket_app.templates.generic')
    def tbl_insurers(self, *args, **kwargs):
        html = self.get_active_tbl_insurer_html(*args, **kwargs)
        javascript = self.get_javascript_tbl_insurer_onload()
        title = "Tbl_insurer"
        return dict(title=title, html=html, javascript=javascript)

    @expose()
    def get_active_tbl_insurer_html(self, *args, **kwargs):
        usernow = request.identity['user']
        dbase_query = self.get_active_tbl_insurer_list(*args, **kwargs)
        outputlist = []
        for item in dbase_query:
            outputlist.append({
                'entity_organisation_id' : item.entity_organisation_id,
                             })
        dbcolumnlist=[
                'entity_organisation_id',
                    ]
        theadlist=[
                'Entity_Organisation_Id',
                ]
        tbl_insurertable = build_html_table(outputlist, dbcolumnlist, theadlist, "tbl_insurer_table")
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-6">
                            <h4 class="card-title">Tbl_insurer</h4>
                        </div>
                        <div class="col-md-6 text-right">
                            <button id="create_new_tbl_insurer" class="btn btn-primary ml-auto">Create a new Tbl_insurer</button>
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
                        {tbl_insurertable}
                    </div>
                </div>
                </div>
            </div>
            <div id='dialogdiv'></div>
        """
        return html

    @expose()
    def get_javascript_tbl_insurer_onload(self, *args, **kwargs):
        javascript = """
        $("#create_new_tbl_insurer").click(function(){
            $('#dialogdiv').load('/entity/get_modal_new_tbl_insurer?', function(data){
                return false;
            });
        });
        $(".tbl_insurer_edit").click(function(){
            var kwargs = 'tbl_insurer_id='+$(this).attr('tbl_insurer_id');
            $('#dialogdiv').load('/entity/get_modal_edit_tbl_insurer?'+kwargs, function(data){
                return false;
            });
        });
        """
        return javascript

    @expose()
    def get_modal_new_tbl_insurer(self, *args, **kwargs):
        html = """
        <div class="modal fade" id="dialog_new_tbl_insurer" tabindex="-1" role="dialog" aria-labelledby="mytbl_insurerLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-6">
                            <h4 class="card-title">New Tbl_insurer</h4>
                        </div>
                    </div>
                    <div class="modal-body">
                        <form id='form_new_tbl_insurer'>
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="entity_organisation_id">Entity_Organisation_Id</label>
						<div class="col-md-9">
							<input id="entity_organisation_id" type="text" name="entity_organisation_id" class="form-control" required='true'>
						</div>
					</div>
				</div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button id='save_new_tbl_insurer' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary tbl_insurer_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
        setFormValidation('#form_new_tbl_insurer');
        $('#save_new_tbl_insurer').click(function(){
             var valid = FormIsValid("#form_new_tbl_insurer");
             if(valid){
                var formserial = getFormData('#form_new_tbl_insurer');
                var data = {data : JSON.stringify(formserial)};

                $.post('/entity/save_new_tbl_insurer?', data, function(data){
                    var result = JSON.parse(data);
                    if(result.success === true){
                        $.redirect('/entity/tbl_insurers');
                    };
                    return false;
                });
             }
        });
        $('.tbl_insurer_back').click(function(){
            $('#dialog_new_tbl_insurer').modal('hide');
        });
        $('#dialog_new_tbl_insurer').modal();
        </script>
     	"""
        return html + javascript

    @expose()
    def get_modal_edit_tbl_insurer(self, *args, **kwargs):
        tbl_insurer_id = kwargs.get('tbl_insurer_id', None)
        if not tbl_insurer_id: return ''
        this = self.get_tbl_insurer_by_id(*args, **kwargs)
        if not this: return ''
        checked = 'checked' if this.active else ''
        html = f"""
        <div class="modal fade" id="dialog_edit_tbl_insurer" tabindex="-1" role="dialog" aria-labelledby="mytbl_insurerLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-6">
                            <h4 class="card-title">New Tbl_insurer</h4>
                        </div>
                    </div>
                    <div class="modal-body">
                        <form id='form_edit_tbl_insurer'>
                            <div style='display: none' class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="tbl_insurer_id">Id</label>
						<div class="col-md-9">
							<input id="id" type="text" name="tbl_insurer_id" value="{this.id}" class="form-control" required='true'>
						</div>
					</div>
				</div>
                            <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="entity_organisation_id">Entity_Organisation_Id</label>
						<div class="col-md-9">
							<input id="entity_organisation_id" type="text" name="entity_organisation_id" value="{this.entity_organisation_id}" class="form-control" required='true'>
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
                        <button id='save_edit_tbl_insurer' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary tbl_insurer_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
        setFormValidation('#form_edit_tbl_insurer');
        $('#save_edit_tbl_insurer').click(function(){
             var valid = FormIsValid("#form_edit_tbl_insurer");
             if(valid){
                var formserial = getFormData('#form_edit_tbl_insurer');
                var data = {data : JSON.stringify(formserial)};

                $.post('/entity/save_edit_tbl_insurer?', data, function(data){
                    var result = JSON.parse(data);
                    if(result.success === true){
                        $.redirect('/entity/tbl_insurers');
                    };
                    return false;
                });
             }
        });
        $('.tbl_insurer_back').click(function(){
            $('#dialog_edit_tbl_insurer').modal('hide');
        });
        $('#dialog_edit_tbl_insurer').modal();
        </script>
     	"""
        return html + javascript

    @expose()
    def save_new_tbl_insurer(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        if not data: return json.dumps({'success' : False, 'data' : 'No data provided'})
        usernow = request.identity['user']
        this = Insurer()
        this.entity_organisation_id = data.get('entity_organisation_id', None)
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()
        return json.dumps({'success' : True, 'data' : this.id})

    @expose()
    def save_edit_tbl_insurer(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        if not data: return json.dumps({'success' : False, 'data' : 'No data provided'})
        usernow = request.identity['user']
        this = self.get_tbl_insurer_by_id(**data)
        if not this: return json.dumps({'success' : False, 'data' : 'No tbl_insurer found for id provided'})
        this.entity_organisation_id = data.get('entity_organisation_id', None)
        if not data.get('active', None): this.active = False
        DBSession.flush()
        return json.dumps({'success' : True, 'data' : this.id})

    @expose()
    def get_tbl_insurer_by_id(self, *args, **kwargs):
        return DBSession.query(Insurer). \
            filter(Insurer.id==kwargs.get('tbl_insurer_id', None)). \
            first()

    @expose()
    def get_active_tbl_insurer_list(self, *args, **kwargs):
        searchphrase = kwargs.get('searchphrase', None)

        tbl_insurer_entity_organisation_id = kwargs.get('tbl_insurer_entity_organisation_id', None)

        if tbl_insurer_entity_organisation_id:
            dbase_query = DBSession.query(Insurer). \
		    filter(Insurer.tbl_insurer_entity_organisation_id==tbl_insurer_entity_organisation_id). \
                        filter(Insurer.active==1). \
		    order_by(asc(Insurer.tbl_insurer_id)).limit(LIMIT)
        else:
            dbase_query = DBSession.query(Insurer). \
                filter(Insurer.active==1). \
                order_by(asc(Insurer.id)). \
                limit(LIMIT)
        return dbase_query
