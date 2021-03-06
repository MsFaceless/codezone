#class_name = ProductAllocation
#table_name = allocations
#prefix =PRE
#postfix =POST
#columns_to_create = [id,name] #id - primary_key autoincrement=True
#cont_name = product
#html_template_name = generic
#dbsession = DBSession
#controller_name = ProductController
#view_cols_list = [name]
#search_cols_list = [name]
#pdf_cols_list = [name]
#link_to_id_or_None = None
#link_class_name_None = None
"""
@q: 1ggf=wv$h"ay 2ggf=wv$h"by 3ggf=wv$h"cy 4ggf=wv$h"dy 5ggf[wvt]"ey 6ggf=wv$h"fy 7ggf=wv$h"gy 8ggf=wv$h"hy 9ggf=wv$h"iy 10ggf[wvt]"jy 11ggf[wvt]"ky 12ggf[wvt]"ly
@w: "api "bgpi "cgp i "dgp i "egpi "fgp i "ggp i "hgp i "igp i "jpi "kpi "lpi
@t: 23ggVGd22ggo_tgcreateclas
@r: 16ggf:wv$"qy 17ggf:wv$"wy 18ggf:wv$"ty @q@t
Instructions: run @r then complete the snip with <ctr-l> then <escape> then @w
"""
##################################################################################################################
#class_name = ProductAllocation
#table_name =allocations
#prefix =PRE
#postfix =POST
#columns_to_create = [id,name] #id - primary_key autoincrement=True
#cont_name =product
#html_template_name =generic
#dbsession =DBSession
#controller_name =ProductController
#view_cols_list = [name]
#search_cols_list = [name]
#pdf_cols_list = [name]
#link_to_id_or_None =
#link_class_name_None =

############################
# Controller
############################


class ProductController(BaseController):
    """Docstring for product."""

    def __init__(self, *args, **kwargs):
        pass

    @require(predicates.not_anonymous())
    @expose('rocket_app.templates.generic')
    def allocations(self, *args, **kwargs):
        html = self.get_active_allocations_html(*args, **kwargs)
        javascript = self.get_javascript_allocations_onload()
        title = "allocations"
        return dict(title=title, html=html, javascript=javascript)

    @expose()
    def get_active_allocations_html(self, *args, **kwargs):
        usernow = request.identity['user']
        dbase_query = self.get_active_allocations_list(*args, **kwargs)
        outputlist = []
        for item in dbase_query:
            outputlist.append({ 
                'name' : item.name, 
                             })
        dbcolumnlist=[ 
                'name', 
                    ]
        theadlist=[ 
                'Name', 
                ]
        allocationstable = build_html_table(outputlist, dbcolumnlist, theadlist, "allocations_table")
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-6">
                            <h4 class="card-title">allocations</h4>
                        </div>
                        <div class="col-md-6 text-right">
                            <button id="create_new_allocations" class="btn btn-primary ml-auto">Create a new allocations</button>
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
                        {allocationstable}
                    </div>
                </div>
                </div>
            </div>
            <div id='dialogdiv'></div>
        """
        return html

    @expose()
    def get_javascript_allocations_onload(self, *args, **kwargs):
        javascript = """
        $("#create_new_allocations").click(function(){
            $('#dialogdiv').load('/product/get_modal_new_allocations?', function(data){
                return false;
            });
        });
        $(".allocations_edit").click(function(){
            var kwargs = 'allocations_id='+$(this).attr('allocations_id');
            $('#dialogdiv').load('/product/get_modal_edit_allocations?'+kwargs, function(data){
                return false;
            });
        });
        """
        return javascript

    @expose()
    def get_modal_new_allocations(self, *args, **kwargs):
        html = """
        <div class="modal fade" id="dialog_new_allocations" tabindex="-1" role="dialog" aria-labelledby="myallocationsLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-6">
                            <h4 class="card-title">New allocations</h4>
                        </div>
                    </div>
                    <div class="modal-body">
                        <form id='form_new_allocations'> 
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
                        <button id='save_new_allocations' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary allocations_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
        setFormValidation('#form_new_allocations'); 
        $('#save_new_allocations').click(function(){
             var valid = FormIsValid("#form_new_allocations");
             if(valid){
                var formserial = getFormData('#form_new_allocations');
                var data = {data : JSON.stringify(formserial)};

                $.post('/product/save_new_allocations?', data, function(data){
                    var result = JSON.parse(data);
                    if(result.success === true){
                        $.redirect('/product/allocations');
                    };
                    return false;
                });
             }
        });
        $('.allocations_back').click(function(){
            $('#dialog_new_allocations').modal('hide');
        });
        $('#dialog_new_allocations').modal();
        </script>
     	"""
        return html + javascript

    @expose()
    def get_modal_edit_allocations(self, *args, **kwargs):
        allocations_id = kwargs.get('allocations_id', None)
        if not allocations_id: return ''
        this = self.get_allocations_by_id(*args, **kwargs)
        if not this: return ''
        checked = 'checked' if this.active else ''
        html = f"""
        <div class="modal fade" id="dialog_edit_allocations" tabindex="-1" role="dialog" aria-labelledby="myallocationsLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-6">
                            <h4 class="card-title">New allocations</h4>
                        </div>
                    </div>
                    <div class="modal-body">
                        <form id='form_edit_allocations'> 
                            <div style='display:none' class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="allocations_id">Id</label>
						<div class="col-md-9">
							<input id="id" type="text" name="allocations_id" value="{this.id}" class="form-control" required='true'>
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
                        <button id='save_edit_allocations' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary allocations_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
        setFormValidation('#form_edit_allocations'); 
        $('#save_edit_allocations').click(function(){
             var valid = FormIsValid("#form_edit_allocations");
             if(valid){
                var formserial = getFormData('#form_edit_allocations');
                var data = {data : JSON.stringify(formserial)};

                $.post('/product/save_edit_allocations?', data, function(data){
                    var result = JSON.parse(data);
                    if(result.success === true){
                        $.redirect('/product/allocations');
                    };
                    return false;
                });
             }
        });
        $('.allocations_back').click(function(){
            $('#dialog_edit_allocations').modal('hide');
        });
        $('#dialog_edit_allocations').modal();
        </script>
     	"""
        return html + javascript

    @expose()
    def save_new_allocations(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        if not data: return json.dumps({'success' : False, 'data' : 'No data provided'})
        usernow = request.identity['user']
        this = ProductAllocation()
        this.name = data.get('name', None)
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()
        return json.dumps({'success' : True, 'data' : this.id})

    @expose()
    def save_edit_allocations(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        if not data: return json.dumps({'success' : False, 'data' : 'No data provided'})
        usernow = request.identity['user']
        this = self.get_allocations_by_id(**data)
        if not this: return json.dumps({'success' : False, 'data' : 'No allocations found for id provided'}) 
        this.name = data.get('name', None)
        if not data.get('active', None): this.active = False
        DBSession.flush()
        return json.dumps({'success' : True, 'data' : this.id})

    @expose()
    def get_allocations_by_id(self, *args, **kwargs):
        return DBSession.query(ProductAllocation). \
            filter(ProductAllocation.id==kwargs.get('allocations_id', None)). \
            first()

    @expose()
    def get_active_allocations_list(self, *args, **kwargs):
        searchphrase = kwargs.get('searchphrase', None)

        name = kwargs.get('name', None)

        if name:
            searchphrase = "%"+kwargs['name']+"%" 
            dbase_query = DBSession.query(ProductAllocation). \
			filter(ProductAllocation.name.like(searchphrase)). \
                        filter(ProductAllocation.active==1). \
			order_by(asc(ProductAllocation.name)).limit(LIMIT)
        else:
            dbase_query = DBSession.query(ProductAllocation). \
                filter(ProductAllocation.active==1). \
                order_by(asc(ProductAllocation.id)). \
                limit(LIMIT)
        return dbase_query
