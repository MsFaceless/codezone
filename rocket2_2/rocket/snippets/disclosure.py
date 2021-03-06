# class_name = EntityIntermediaryDisclosure
# table_name = intermediary_disclosure
# prefix =PRE
# postfix =POST
# columns_to_create = [id, text] #id - primary_key autoincrement=True
# cont_name = setup
# html_template_name = generic
# dbsession = DBSession
# controller_name = SetupController
# view_cols_list = [text]
# search_cols_list = [text]
# pdf_cols_list = [text]
# link_to_id_or_None = None
# link_class_name_None = None
"""
@q: 1ggf=wv$h"ay 2ggf=wv$h"by 3ggf=wv$h"cy 4ggf=wv$h"dy 5ggf[wvt]"ey 6ggf=wv$h"fy 7ggf=wv$h"gy 8ggf=wv$h"hy 9ggf=wv$h"iy 10ggf[wvt]"jy 11ggf[wvt]"ky 12ggf[wvt]"ly
@w: "api "bgpi "cgp i "dgp i "egpi "fgp i "ggp i "hgp i "igp i "jpi "kpi "lpi
@t: 23ggVGd22ggo_tgcreateclas
@r: 16ggf: wv$"qy 17ggf: wv$"wy 18ggf: wv$"ty @q@t
Instructions: run @r then complete the snip with <ctr-l> then <escape> then @w
"""


##################################################################################################################
# class_name = EntityIntermediaryDisclosure
# table_name =intermediary_disclosure
# prefix =PRE
# postfix =POST
# columns_to_create = [id, text] #id - primary_key autoincrement=True
# cont_name =setup
# html_template_name =generic
# dbsession =DBSession
# controller_name =SetupController
# view_cols_list = [text]
# search_cols_list = [text]
# pdf_cols_list = [text]
# link_to_id_or_None =
# link_class_name_None =

############################
# Controller
############################


class SetupController(BaseController):
    """Docstring for setup."""

    def __init__(self, *args, **kwargs):
        pass

    @require(predicates.not_anonymous())
    @expose('rocket.templates.generic')
    def intermediary_disclosure(self, *args, **kwargs):
        html = self.get_active_intermediary_disclosure_html(*args, **kwargs)
        javascript = self.get_javascript_intermediary_disclosure_onload()
        title = "intermediary_disclosure"
        return dict(title=title, html=html, javascript=javascript)

    @expose()
    def get_active_intermediary_disclosure_html(self, *args, **kwargs):
        usernow = request.identity['user']
        dbase_query = self.get_active_intermediary_disclosure_list(*args, **kwargs)
        outputlist = []
        for item in dbase_query:
            outputlist.append({
                'text': "<div class='edit intermediary_disclosure_edit' intermediary_disclosure_id='{1}'>{0}</div>".format(
                    item.text, item.id),
            })
        dbcolumnlist = [
            'text',
        ]
        theadlist = [
            'Text',
        ]
        intermediary_disclosuretable = build_html_table(outputlist, dbcolumnlist, theadlist,
                                                                   "intermediary_disclosure_table")
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-6">
                            <h4 class="card-title">intermediary_disclosure</h4>
                        </div>
                        <div class="col-md-6 text-right">
                            <button id="create_new_intermediary_disclosure" class="btn btn-primary ml-auto">Create a New intermediary_disclosure</button>
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
                        {intermediary_disclosuretable}
                    </div>
                </div>
                </div>
            </div>
            <div id='dialogdiv'></div>
        """
        return html

    @expose()
    def get_javascript_intermediary_disclosure_onload(self, *args, **kwargs):
        javascript = """
        $("#create_new_intermediary_disclosure").click(function(){
            $('#dialogdiv').load('/setup/get_modal_new_intermediary_disclosure?', function(data){
                return false;
            });
        });
        $(".intermediary_disclosure_edit").click(function(){
            var kwargs = 'intermediary_disclosure_id='+$(this).attr('intermediary_disclosure_id');
            $('#dialogdiv').load('/setup/get_modal_edit_intermediary_disclosure?'+kwargs, function(data){
                return false;
            });
        });
        """
        return javascript

    @expose()
    def get_modal_new_intermediary_disclosure(self, *args, **kwargs):
        html = """
        <div class="modal fade" id="dialog_new_intermediary_disclosure" tabindex="-1" role="dialog" aria-labelledby="myintermediary_disclosureLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-6">
                            <h4 class="card-title">New intermediary_disclosure</h4>
                        </div>
                    </div>
                    <div class="modal-body">
                        <form id='form_new_intermediary_disclosure'> 
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="text">Text</label>
						<div class="col-md-9">
							<input id="text" type="text" name="text" class="form-control" required='true'>
						</div>
					</div>
				</div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button id='save_new_intermediary_disclosure' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary intermediary_disclosure_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
        setFormValidation('#form_new_intermediary_disclosure'); 
        $('#save_new_intermediary_disclosure').click(function(){
             var valid = FormIsValid("#form_new_intermediary_disclosure");
             if(valid){
                var formserial = getFormData('#form_new_intermediary_disclosure');
                var data = {data : JSON.stringify(formserial)};

                $.post('/setup/save_new_intermediary_disclosure?', data, function(data){
                    var result = JSON.parse(data);
                    if(result.success === true){
                        $.redirect('/setup/intermediary_disclosure');
                    };
                    return false;
                });
             }
        });
        $('.intermediary_disclosure_back').click(function(){
            $('#dialog_new_intermediary_disclosure').modal('hide');
        });
        $('#dialog_new_intermediary_disclosure').modal();
        </script>
     	"""
        return html + javascript

    @expose()
    def get_modal_edit_intermediary_disclosure(self, *args, **kwargs):
        intermediary_disclosure_id = kwargs.get('intermediary_disclosure_id', None)
        if not intermediary_disclosure_id: return ''
        this = self.get_intermediary_disclosure_by_id(*args, **kwargs)
        if not this: return ''
        checked = 'checked' if this.active else ''
        html = f"""
        <div class="modal fade" id="dialog_edit_intermediary_disclosure" tabindex="-1" role="dialog" aria-labelledby="myintermediary_disclosureLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-6">
                            <h4 class="card-title">New intermediary_disclosure</h4>
                        </div>
                    </div>
                    <div class="modal-body">
                        <form id='form_edit_intermediary_disclosure'> 
                            <div style='display:none' class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="intermediary_disclosure_id">Id</label>
						<div class="col-md-9">
							<input id="id" type="text" name="intermediary_disclosure_id" value="{this.id}" class="form-control" required='true'>
						</div>
					</div>
				</div>
                            <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="text"> Text</label>
						<div class="col-md-9">
							<input id="text" type="text" name="text" value="{this.text}" class="form-control" required='true'>
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
                        <button id='save_edit_intermediary_disclosure' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary intermediary_disclosure_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
        setFormValidation('#form_edit_intermediary_disclosure'); 
        $('#save_edit_intermediary_disclosure').click(function(){
             var valid = FormIsValid("#form_edit_intermediary_disclosure");
             if(valid){
                var formserial = getFormData('#form_edit_intermediary_disclosure');
                var data = {data : JSON.stringify(formserial)};

                $.post('/setup/save_edit_intermediary_disclosure?', data, function(data){
                    var result = JSON.parse(data);
                    if(result.success === true){
                        $.redirect('/setup/intermediary_disclosure');
                    };
                    return false;
                });
             }
        });
        $('.intermediary_disclosure_back').click(function(){
            $('#dialog_edit_intermediary_disclosure').modal('hide');
        });
        $('#dialog_edit_intermediary_disclosure').modal();
        </script>
     	"""
        return html + javascript

    @expose()
    def save_new_intermediary_disclosure(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        if not data: return json.dumps({'success': False, 'data': 'No data provided'})
        usernow = request.identity['user']
        this = EntityIntermediaryDisclosure()
        this.text = data.get('text', None)
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()
        return json.dumps({'success': True, 'data': this.id})

    @expose()
    def save_edit_intermediary_disclosure(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        if not data: return json.dumps({'success': False, 'data': 'No data provided'})
        usernow = request.identity['user']
        this = self.get_intermediary_disclosure_by_id(**data)
        if not this: return json.dumps(
            {'success': False, 'data': 'No intermediary_disclosure found for id provided'})
        this.text = data.get('text', None)
        if not data.get('active', None): this.active = False
        DBSession.flush()
        return json.dumps({'success': True, 'data': this.id})

    @expose()
    def get_intermediary_disclosure_by_id(self, *args, **kwargs):
        return DBSession.query(EntityIntermediaryDisclosure). \
            filter(EntityIntermediaryDisclosure.id == kwargs.get('intermediary_disclosure_id', None)). \
            first()

    @expose()
    def get_active_intermediary_disclosure_list(self, *args, **kwargs):
        searchphrase = kwargs.get('searchphrase', None)

        text = kwargs.get('text', None)

        if text:
            searchphrase = "%" + kwargs['text'] + "%"
            dbase_query = DBSession.query(EntityIntermediaryDisclosure). \
                filter(EntityIntermediaryDisclosure.text.like(searchphrase)). \
                filter(EntityIntermediaryDisclosure.active == 1). \
                order_by(asc(EntityIntermediaryDisclosure.text)).limit(LIMIT)
        else:
            dbase_query = DBSession.query(EntityIntermediaryDisclosure). \
                filter(EntityIntermediaryDisclosure.active == 1). \
                order_by(asc(EntityIntermediaryDisclosure.id)). \
                limit(LIMIT)
        return dbase_query
