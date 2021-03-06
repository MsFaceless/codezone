#class_name = TextMerge
#table_name = tbl_text_merge
#prefix =PRE
#postfix =POST
#columns_to_create = [id, code, name] #id - primary_key autoincrement=True
#cont_name = setup
#html_template_name = generic
#dbsession = DBSession
#controller_name = SetupController
#view_cols_list = [code, name]
#search_cols_list = [code, name]
#pdf_cols_list = [code, name]
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
#class_name = TextMerge
#table_name =tbl_text_merge
#prefix =PRE
#postfix =POST
#columns_to_create = [id, code, name] #id - primary_key autoincrement=True
#cont_name =setup
#html_template_name =generic
#dbsession =DBSession
#controller_name =SetupController
#view_cols_list = [code, name]
#search_cols_list = [code, name]
#pdf_cols_list = [code, name]
#link_to_id_or_None =
#link_class_name_None =

############################
# Controller
############################


class SetupController(BaseController):
    """Docstring for setup ."""

    def __init__(self, *args, **kwargs):
        pass

    @require(predicates.not_anonymous())
    @expose('rocket_app.templates.generic')
    def tbl_text_merges(self, *args, **kwargs):
        html = self.get_active_tbl_text_merge_html(*args, **kwargs)
        javascript = self.get_javascript_tbl_text_merge_onload()
        title = "Tbl_text_merge"
        return dict(title=title, html=html, javascript=javascript)

    @expose()
    def get_active_tbl_text_merge_html(self, *args, **kwargs):
        usernow = request.identity['user']
        dbase_query = self.get_active_tbl_text_merge_list(*args, **kwargs)
        outputlist = []
        for item in dbase_query:
            outputlist.append({
                'code' : "<div class='edit tbl_text_merge_edit' tbl_text_merge_id='{1}'>{0}</div>".format(item.code, item.id),
                'name' : item.name,
                             })
        dbcolumnlist=[
                'code',
                'name',
                    ]
        theadlist=[
                'Code',
                'Name',
                ]
        tbl_text_mergetable = build_html_table(outputlist, dbcolumnlist, theadlist, "tbl_text_merge_table")
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-6">
                            <h4 class="card-title">Tbl_text_merge</h4>
                        </div>
                        <div class="col-md-6 text-right">
                            <button id="create_new_tbl_text_merge" class="btn btn-primary ml-auto">Create a new Tbl_text_merge</button>
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
                        {tbl_text_mergetable}
                    </div>
                </div>
                </div>
            </div>
            <div id='dialogdiv'></div>
        """
        return html

    @expose()
    def get_javascript_tbl_text_merge_onload(self, *args, **kwargs):
        javascript = """
        $("#create_new_tbl_text_merge").click(function(){
            $('#dialogdiv').load('/setup /get_modal_new_tbl_text_merge?', function(data){
                return false;
            });
        });
        $(".tbl_text_merge_edit").click(function(){
            var kwargs = 'tbl_text_merge_id='+$(this).attr('tbl_text_merge_id');
            $('#dialogdiv').load('/setup /get_modal_edit_tbl_text_merge?'+kwargs, function(data){
                return false;
            });
        });
        """
        return javascript

    @expose()
    def get_modal_new_tbl_text_merge(self, *args, **kwargs):
        html = """
        <div class="modal fade" id="dialog_new_tbl_text_merge" tabindex="-1" role="dialog" aria-labelledby="mytbl_text_mergeLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-6">
                            <h4 class="card-title">New Tbl_text_merge</h4>
                        </div>
                    </div>
                    <div class="modal-body">
                        <form id='form_new_tbl_text_merge'>
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
						<label class="col-md-3 col-form-label" required for="name">Name</label>
						<div class="col-md-9">
							<input id="name" type="text" name="name" class="form-control" required='true'>
						</div>
					</div>
				</div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button id='save_new_tbl_text_merge' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary tbl_text_merge_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
        setFormValidation('#form_new_tbl_text_merge');
        $('#save_new_tbl_text_merge').click(function(){
             var valid = FormIsValid("#form_new_tbl_text_merge");
             if(valid){
                var formserial = getFormData('#form_new_tbl_text_merge');
                var data = {data : JSON.stringify(formserial)};

                $.post('/setup /save_new_tbl_text_merge?', data, function(data){
                    var result = JSON.parse(data);
                    if(result.success === true){
                        $.redirect('/setup /tbl_text_merges');
                    };
                    return false;
                });
             }
        });
        $('.tbl_text_merge_back').click(function(){
            $('#dialog_new_tbl_text_merge').modal('hide');
        });
        $('#dialog_new_tbl_text_merge').modal();
        </script>
     	"""
        return html + javascript

    @expose()
    def get_modal_edit_tbl_text_merge(self, *args, **kwargs):
        tbl_text_merge_id = kwargs.get('tbl_text_merge_id', None)
        if not tbl_text_merge_id: return ''
        this = self.get_tbl_text_merge_by_id(*args, **kwargs)
        if not this: return ''
        checked = 'checked' if this.active else ''
        html = f"""
        <div class="modal fade" id="dialog_edit_tbl_text_merge" tabindex="-1" role="dialog" aria-labelledby="mytbl_text_mergeLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-6">
                            <h4 class="card-title">New Tbl_text_merge</h4>
                        </div>
                    </div>
                    <div class="modal-body">
                        <form id='form_edit_tbl_text_merge'>
                            <div style='display: none' class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="tbl_text_merge_id">Id</label>
						<div class="col-md-9">
							<input id="id" type="text" name="tbl_text_merge_id" value="{this.id}" class="form-control" required='true'>
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
						<label class="col-md-3 col-form-label" required for="name">Name</label>
						<div class="col-md-9">
							<input id="name" type="text" name="name" value="{this.name}" class="form-control" required='true'>
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
                        <button id='save_edit_tbl_text_merge' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary tbl_text_merge_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
        setFormValidation('#form_edit_tbl_text_merge');
        $('#save_edit_tbl_text_merge').click(function(){
             var valid = FormIsValid("#form_edit_tbl_text_merge");
             if(valid){
                var formserial = getFormData('#form_edit_tbl_text_merge');
                var data = {data : JSON.stringify(formserial)};

                $.post('/setup /save_edit_tbl_text_merge?', data, function(data){
                    var result = JSON.parse(data);
                    if(result.success === true){
                        $.redirect('/setup /tbl_text_merges');
                    };
                    return false;
                });
             }
        });
        $('.tbl_text_merge_back').click(function(){
            $('#dialog_edit_tbl_text_merge').modal('hide');
        });
        $('#dialog_edit_tbl_text_merge').modal();
        </script>
     	"""
        return html + javascript

    @expose()
    def save_new_tbl_text_merge(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        if not data: return json.dumps({'success' : False, 'data' : 'No data provided'})
        usernow = request.identity['user']
        this = TextMerge()
        this.code = data.get('code', None)
        this.name = data.get('name', None)
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()
        return json.dumps({'success' : True, 'data' : this.id})

    @expose()
    def save_edit_tbl_text_merge(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        if not data: return json.dumps({'success' : False, 'data' : 'No data provided'})
        usernow = request.identity['user']
        this = self.get_tbl_text_merge_by_id(**data)
        if not this: return json.dumps({'success' : False, 'data' : 'No tbl_text_merge found for id provided'})
        this.code = data.get('code', None)
        this.name = data.get('name', None)
        if not data.get('active', None): this.active = False
        DBSession.flush()
        return json.dumps({'success' : True, 'data' : this.id})

    @expose()
    def get_tbl_text_merge_by_id(self, *args, **kwargs):
        return DBSession.query(TextMerge). \
            filter(TextMerge.id==kwargs.get('tbl_text_merge_id', None)). \
            first()

    @expose()
    def get_active_tbl_text_merge_list(self, *args, **kwargs):
        searchphrase = kwargs.get('searchphrase', None)

        code = kwargs.get('code', None)
        name = kwargs.get('name', None)

        if code:
            searchphrase = "%"+kwargs['code']+"%"
            dbase_query = DBSession.query(TextMerge). \
			filter(TextMerge.code.like(searchphrase)). \
                        filter(TextMerge.active==1). \
			order_by(asc(TextMerge.code)).limit(LIMIT)
        if name:
            searchphrase = "%"+kwargs['name']+"%"
            dbase_query = DBSession.query(TextMerge). \
			filter(TextMerge.name.like(searchphrase)). \
                        filter(TextMerge.active==1). \
			order_by(asc(TextMerge.name)).limit(LIMIT)
        else:
            dbase_query = DBSession.query(TextMerge). \
                filter(TextMerge.active==1). \
                order_by(asc(TextMerge.id)). \
                limit(LIMIT)
        return dbase_query
