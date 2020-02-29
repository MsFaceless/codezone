#class_name = ProductPremiumRate
#table_name = tbl_product_premium_rate
#prefix =PRE
#postfix =POST
#columns_to_create = [id, code, name, base_value] #id - primary_key autoincrement=True
#cont_name = setup
#html_template_name = generic
#dbsession = DBSession
#controller_name = SetupController
#view_cols_list = [code, name, base_value]
#search_cols_list = [code, name, base_value]
#pdf_cols_list = [code, name, base_value]
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
#class_name = ProductPremiumRate
#table_name =tbl_product_premium_rate
#prefix =PRE
#postfix =POST
#columns_to_create = [id, code, name, base_value] #id - primary_key autoincrement=True
#cont_name =setup
#html_template_name =generic
#dbsession =DBSession
#controller_name =SetupController
#view_cols_list = [code, name, base_value]
#search_cols_list = [code, name, base_value]
#pdf_cols_list = [code, name, base_value]
#link_to_id_or_None =
#link_class_name_None =

############################
# Controller
############################


class SetupController(BaseController):
    """Docstring for setup."""

    def __init__(self, *args, **kwargs):
        pass

    @require(predicates.not_anonymous())
    @expose('rocket.templates.generic')
    def tbl_product_premium_rates(self, *args, **kwargs):
        html = self.get_active_tbl_product_premium_rate_html(*args, **kwargs)
        javascript = self.get_javascript_tbl_product_premium_rate_onload()
        title = "Tbl_product_premium_rate"
        return dict(title=title, html=html, javascript=javascript)

    @expose()
    def get_active_tbl_product_premium_rate_html(self, *args, **kwargs):
        usernow = request.identity['user']
        dbase_query = self.get_active_tbl_product_premium_rate_list(*args, **kwargs)
        outputlist = []
        for item in dbase_query:
            outputlist.append({
                'code' : "<div class='edit tbl_product_premium_rate_edit' tbl_product_premium_rate_id='{1}'>{0}</div>".format(item.code, item.id),
                'name' : item.name,
                'base_value' : item.base_value,
                             })
        dbcolumnlist=[
                'code',
                'name',
                'base_value',
                    ]
        theadlist=[
                'Code',
                'Name',
                'Base_Value',
                ]
        tbl_product_premium_ratetable = build_html_table(outputlist, dbcolumnlist, theadlist, "tbl_product_premium_rate_table")
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-6">
                            <h4 class="card-title">Tbl_product_premium_rate</h4>
                        </div>
                        <div class="col-md-6 text-right">
                            <button id="create_new_tbl_product_premium_rate" class="btn btn-primary ml-auto">Create a new Tbl_product_premium_rate</button>
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
                        {tbl_product_premium_ratetable}
                    </div>
                </div>
                </div>
            </div>
            <div id='dialogdiv'></div>
        """
        return html

    @expose()
    def get_javascript_tbl_product_premium_rate_onload(self, *args, **kwargs):
        javascript = """
        $("#create_new_tbl_product_premium_rate").click(function(){
            $('#dialogdiv').load('/setup/get_modal_new_tbl_product_premium_rate?', function(data){
                return false;
            });
        });
        $(".tbl_product_premium_rate_edit").click(function(){
            var kwargs = 'tbl_product_premium_rate_id='+$(this).attr('tbl_product_premium_rate_id');
            $('#dialogdiv').load('/setup/get_modal_edit_tbl_product_premium_rate?'+kwargs, function(data){
                return false;
            });
        });
        """
        return javascript

    @expose()
    def get_modal_new_tbl_product_premium_rate(self, *args, **kwargs):
        html = """
        <div class="modal fade" id="dialog_new_tbl_product_premium_rate" tabindex="-1" role="dialog" aria-labelledby="mytbl_product_premium_rateLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-6">
                            <h4 class="card-title">New Tbl_product_premium_rate</h4>
                        </div>
                    </div>
                    <div class="modal-body">
                        <form id='form_new_tbl_product_premium_rate'>
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
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="base_value">Base_Value</label>
						<div class="col-md-9">
							<input id="base_value" type="text" name="base_value" class="form-control" required='true'>
						</div>
					</div>
				</div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button id='save_new_tbl_product_premium_rate' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary tbl_product_premium_rate_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
        setFormValidation('#form_new_tbl_product_premium_rate');
        $('#save_new_tbl_product_premium_rate').click(function(){
             var valid = FormIsValid("#form_new_tbl_product_premium_rate");
             if(valid){
                var formserial = getFormData('#form_new_tbl_product_premium_rate');
                var data = {data : JSON.stringify(formserial)};

                $.post('/setup/save_new_tbl_product_premium_rate?', data, function(data){
                    var result = JSON.parse(data);
                    if(result.success === true){
                        $.redirect('/setup/tbl_product_premium_rates');
                    };
                    return false;
                });
             }
        });
        $('.tbl_product_premium_rate_back').click(function(){
            $('#dialog_new_tbl_product_premium_rate').modal('hide');
        });
        $('#dialog_new_tbl_product_premium_rate').modal();
        </script>
     	"""
        return html + javascript

    @expose()
    def get_modal_edit_tbl_product_premium_rate(self, *args, **kwargs):
        tbl_product_premium_rate_id = kwargs.get('tbl_product_premium_rate_id', None)
        if not tbl_product_premium_rate_id: return ''
        this = self.get_tbl_product_premium_rate_by_id(*args, **kwargs)
        if not this: return ''
        checked = 'checked' if this.active else ''
        html = f"""
        <div class="modal fade" id="dialog_edit_tbl_product_premium_rate" tabindex="-1" role="dialog" aria-labelledby="mytbl_product_premium_rateLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-6">
                            <h4 class="card-title">New Tbl_product_premium_rate</h4>
                        </div>
                    </div>
                    <div class="modal-body">
                        <form id='form_edit_tbl_product_premium_rate'>
                            <div style='display:none' class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="tbl_product_premium_rate_id">Id</label>
						<div class="col-md-9">
							<input id="id" type="text" name="tbl_product_premium_rate_id" value="{this.id}" class="form-control" required='true'>
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
                            <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="base_value">Base_Value</label>
						<div class="col-md-9">
							<input id="base_value" type="text" name="base_value" value="{this.base_value}" class="form-control" required='true'>
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
                        <button id='save_edit_tbl_product_premium_rate' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary tbl_product_premium_rate_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
        setFormValidation('#form_edit_tbl_product_premium_rate');
        $('#save_edit_tbl_product_premium_rate').click(function(){
             var valid = FormIsValid("#form_edit_tbl_product_premium_rate");
             if(valid){
                var formserial = getFormData('#form_edit_tbl_product_premium_rate');
                var data = {data : JSON.stringify(formserial)};

                $.post('/setup/save_edit_tbl_product_premium_rate?', data, function(data){
                    var result = JSON.parse(data);
                    if(result.success === true){
                        $.redirect('/setup/tbl_product_premium_rates');
                    };
                    return false;
                });
             }
        });
        $('.tbl_product_premium_rate_back').click(function(){
            $('#dialog_edit_tbl_product_premium_rate').modal('hide');
        });
        $('#dialog_edit_tbl_product_premium_rate').modal();
        </script>
     	"""
        return html + javascript

    @expose()
    def save_new_tbl_product_premium_rate(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        if not data: return json.dumps({'success' : False, 'data' : 'No data provided'})
        usernow = request.identity['user']
        this = ProductPremiumRate()
        this.code = data.get('code', None)
        this.name = data.get('name', None)
        this.base_value = data.get('base_value', None)
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()
        return json.dumps({'success' : True, 'data' : this.id})

    @expose()
    def save_edit_tbl_product_premium_rate(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        if not data: return json.dumps({'success' : False, 'data' : 'No data provided'})
        usernow = request.identity['user']
        this = self.get_tbl_product_premium_rate_by_id(**data)
        if not this: return json.dumps({'success' : False, 'data' : 'No tbl_product_premium_rate found for id provided'})
        this.code = data.get('code', None)
        this.name = data.get('name', None)
        this.base_value = data.get('base_value', None)
        if not data.get('active', None): this.active = False
        DBSession.flush()
        return json.dumps({'success' : True, 'data' : this.id})

    @expose()
    def get_tbl_product_premium_rate_by_id(self, *args, **kwargs):
        return DBSession.query(ProductPremiumRate). \
            filter(ProductPremiumRate.id==kwargs.get('tbl_product_premium_rate_id', None)). \
            first()

    @expose()
    def get_active_tbl_product_premium_rate_list(self, *args, **kwargs):
        searchphrase = kwargs.get('searchphrase', None)

        code = kwargs.get('code', None)
        name = kwargs.get('name', None)
        base_value = kwargs.get('base_value', None)

        if code:
            searchphrase = "%"+kwargs['code']+"%"
            dbase_query = DBSession.query(ProductPremiumRate). \
			filter(ProductPremiumRate.code.like(searchphrase)). \
                        filter(ProductPremiumRate.active==1). \
			order_by(asc(ProductPremiumRate.code)).limit(LIMIT)
        if name:
            searchphrase = "%"+kwargs['name']+"%"
            dbase_query = DBSession.query(ProductPremiumRate). \
			filter(ProductPremiumRate.name.like(searchphrase)). \
                        filter(ProductPremiumRate.active==1). \
			order_by(asc(ProductPremiumRate.name)).limit(LIMIT)
        if base_value:
            searchphrase = "%"+kwargs['base_value']+"%"
            dbase_query = DBSession.query(ProductPremiumRate). \
			filter(ProductPremiumRate.base_value.like(searchphrase)). \
                        filter(ProductPremiumRate.active==1). \
			order_by(asc(ProductPremiumRate.base_value)).limit(LIMIT)
        else:
            dbase_query = DBSession.query(ProductPremiumRate). \
                filter(ProductPremiumRate.active==1). \
                order_by(asc(ProductPremiumRate.id)). \
                limit(LIMIT)
        return dbase_query
