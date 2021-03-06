#class_name = ProductPremiumRateLineItem
#table_name = tbl_product_premium_rate_line_item
#prefix =PRE
#postfix =POST
#columns_to_create = [id, product_premium_rate_id, gender_id, maximum_age, minimum_age, rate_factor] #id - primary_key autoincrement=True
#cont_name = setup
#html_template_name = generic
#dbsession = DBSession
#controller_name = SetupController
#view_cols_list = [product_premium_rate_id, gender_id, maximum_age, minimum_age, rate_factor]
#search_cols_list = [product_premium_rate_id, gender_id, maximum_age, minimum_age, rate_factor]
#pdf_cols_list = [product_premium_rate_id, gender_id, maximum_age, minimum_age, rate_factor]
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
#class_name = ProductPremiumRateLineItem
#table_name =tbl_product_premium_rate_line_item
#prefix =PRE
#postfix =POST
#columns_to_create = [id, product_premium_rate_id, gender_id, maximum_age, minimum_age, rate_factor] #id - primary_key autoincrement=True
#cont_name =setup
#html_template_name =generic
#dbsession =DBSession
#controller_name =SetupController
#view_cols_list = [product_premium_rate_id, gender_id, maximum_age, minimum_age, rate_factor]
#search_cols_list = [product_premium_rate_id, gender_id, maximum_age, minimum_age, rate_factor]
#pdf_cols_list = [product_premium_rate_id, gender_id, maximum_age, minimum_age, rate_factor]
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
    def tbl_product_premium_rate_line_items(self, *args, **kwargs):
        html = self.get_active_tbl_product_premium_rate_line_item_html(*args, **kwargs)
        javascript = self.get_javascript_tbl_product_premium_rate_line_item_onload()
        title = "Tbl_product_premium_rate_line_item"
        return dict(title=title, html=html, javascript=javascript)

    @expose()
    def get_active_tbl_product_premium_rate_line_item_html(self, *args, **kwargs):
        usernow = request.identity['user']
        dbase_query = self.get_active_tbl_product_premium_rate_line_item_list(*args, **kwargs)
        outputlist = []
        for item in dbase_query:
            outputlist.append({
                'product_premium_rate_id' : "<div class='edit tbl_product_premium_rate_line_item_edit' tbl_product_premium_rate_line_item_id='{1}'>{0}</div>".format(item.product_premium_rate_id, item.id),
                'gender_id' : item.gender_id,
                'maximum_age' : item.maximum_age,
                'minimum_age' : item.minimum_age,
                'rate_factor' : item.rate_factor,
                             })
        dbcolumnlist=[
                'product_premium_rate_id',
                'gender_id',
                'maximum_age',
                'minimum_age',
                'rate_factor',
                    ]
        theadlist=[
                'Product_Premium_Rate_Id',
                'Gender_Id',
                'Maximum_Age',
                'Minimum_Age',
                'Rate_Factor',
                ]
        tbl_product_premium_rate_line_itemtable = build_html_table(outputlist, dbcolumnlist, theadlist, "tbl_product_premium_rate_line_item_table")
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-6">
                            <h4 class="card-title">Tbl_product_premium_rate_line_item</h4>
                        </div>
                        <div class="col-md-6 text-right">
                            <button id="create_new_tbl_product_premium_rate_line_item" class="btn btn-primary ml-auto">Create a new Tbl_product_premium_rate_line_item</button>
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
                        {tbl_product_premium_rate_line_itemtable}
                    </div>
                </div>
                </div>
            </div>
        """
        return html

    @expose()
    def get_javascript_tbl_product_premium_rate_line_item_onload(self, *args, **kwargs):
        javascript = """
        $("#create_new_tbl_product_premium_rate_line_item").click(function(){
            $.redirect('/setup/new_tbl_product_premium_rate_line_item');
        });
        $(".tbl_product_premium_rate_line_item_edit").click(function(){
            var data = {tbl_product_premium_rate_line_item_id : $(this).attr('tbl_product_premium_rate_line_item_id')};
            $.redirect('/setup/edit_tbl_product_premium_rate_line_item', data);
        });
        """
        return javascript

    @expose('rocket.templates.generic')
    def new_tbl_product_premium_rate_line_item(self, *args, **kwargs):
        html = """
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-header d-flex">
                        <div class="col-md-6">
                            <h4 class="card-title">New Tbl_product_premium_rate_line_item</h4>
                        </div>
                        <div class="col-md-6 text-right">
                            <button class="btn btn-primary ml-auto action_back tbl_product_premium_rate_line_item_back">Back to Tbl_product_premium_rate_line_item List</button>
                        </div>
                    </div>
                    <div class="card-body">
                        <form id='form_new_tbl_product_premium_rate_line_item'>
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="product_premium_rate_id">Product_Premium_Rate_Id</label>
						<div class="col-md-9">
							<input id="product_premium_rate_id" type="text" name="product_premium_rate_id" class="form-control" required='true'>
						</div>
					</div>
				</div>
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="gender_id">Gender_Id</label>
						<div class="col-md-9">
							<input id="gender_id" type="text" name="gender_id" class="form-control" required='true'>
						</div>
					</div>
				</div>
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="maximum_age">Maximum_Age</label>
						<div class="col-md-9">
							<input id="maximum_age" type="text" name="maximum_age" class="form-control" required='true'>
						</div>
					</div>
				</div>
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="minimum_age">Minimum_Age</label>
						<div class="col-md-9">
							<input id="minimum_age" type="text" name="minimum_age" class="form-control" required='true'>
						</div>
					</div>
				</div>
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="rate_factor">Rate_Factor</label>
						<div class="col-md-9">
							<input id="rate_factor" type="text" name="rate_factor" class="form-control" required='true'>
						</div>
					</div>
				</div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-body">
                        <button id='save_new_tbl_product_premium_rate_line_item' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary tbl_product_premium_rate_line_item_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        setFormValidation('#form_new_tbl_product_premium_rate_line_item');
        $('#save_new_tbl_product_premium_rate_line_item').click(function(){
             var valid = FormIsValid("#form_new_tbl_product_premium_rate_line_item");
             if(valid){
                var formserial = getFormData('#form_new_tbl_product_premium_rate_line_item');
                var data = {data : JSON.stringify(formserial)};

                $.post('/setup/save_new_tbl_product_premium_rate_line_item?', data, function(data){
                    var result = JSON.parse(data);
                    if(result.success === true){
                        $.redirect('/setup/tbl_product_premium_rate_line_items');
                    };
                    return false;
                });
             }
        });
        $('.tbl_product_premium_rate_line_item_back').click(function(){
            $.redirect('/setup/tbl_product_premium_rate_line_items');
        });
     	"""
        title = "New Tbl_product_premium_rate_line_item"
        return dict(title=title, html=html, javascript=javascript)

    @expose('rocket.templates.generic')
    def edit_tbl_product_premium_rate_line_item(self, *args, **kwargs):
        tbl_product_premium_rate_line_item_id = kwargs.get('tbl_product_premium_rate_line_item_id', None)
        if not tbl_product_premium_rate_line_item_id: redirect('/setup/tbl_product_premium_rate_line_items')
        this = self.get_tbl_product_premium_rate_line_item_by_id(*args, **kwargs)
        if not this: redirect('/setup/tbl_product_premium_rate_line_items')
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-header d-flex">
                        <div class="col-md-6">
                            <h4 class="card-title">Edit Tbl_product_premium_rate_line_item</h4>
                        </div>
                        <div class="col-md-6 text-right">
                            <button class="btn btn-primary ml-auto action_back tbl_product_premium_rate_line_item_back">Back to Tbl_product_premium_rate_line_item List</button>
                        </div>
                    </div>
                    <div class="card-body">
                        <form id='form_edit_tbl_product_premium_rate_line_item'>
                                <div style='display:none' class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="tbl_product_premium_rate_line_item_id">Id</label>
						<div class="col-md-9">
							<input id="id" type="text" name="tbl_product_premium_rate_line_item_id" value="{this.id}" class="form-control" required='true'>
						</div>
					</div>
				</div>
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="product_premium_rate_id">Product_Premium_Rate_Id</label>
						<div class="col-md-9">
							<input id="product_premium_rate_id" type="text" name="product_premium_rate_id" value="{this.product_premium_rate_id}" class="form-control" required='true'>
						</div>
					</div>
				</div>
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="gender_id">Gender_Id</label>
						<div class="col-md-9">
							<input id="gender_id" type="text" name="gender_id" value="{this.gender_id}" class="form-control" required='true'>
						</div>
					</div>
				</div>
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="maximum_age">Maximum_Age</label>
						<div class="col-md-9">
							<input id="maximum_age" type="text" name="maximum_age" value="{this.maximum_age}" class="form-control" required='true'>
						</div>
					</div>
				</div>
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="minimum_age">Minimum_Age</label>
						<div class="col-md-9">
							<input id="minimum_age" type="text" name="minimum_age" value="{this.minimum_age}" class="form-control" required='true'>
						</div>
					</div>
				</div>
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="rate_factor">Rate_Factor</label>
						<div class="col-md-9">
							<input id="rate_factor" type="text" name="rate_factor" value="{this.rate_factor}" class="form-control" required='true'>
						</div>
					</div>
				</div>
                            <div class="col-md-12">
                                <div class="form-group row">
                                  <label class="col-3 col-form-label" for="active" required>Active</label>
                                  <div class="col-9"><div class="form-check">
                                      <label class="form-check-label">
                                        <input class="form-check-input" type="checkbox" name="active" id="active" {checked}/></div>
                                      </label>
                                  </div>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-body">
                        <button id='save_edit_tbl_product_premium_rate_line_item' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary tbl_product_premium_rate_line_item_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        setFormValidation('#form_edit_tbl_product_premium_rate_line_item');
        $('#save_edit_tbl_product_premium_rate_line_item').click(function(){
             var valid = FormIsValid("#form_edit_tbl_product_premium_rate_line_item");
             if(valid){
                var formserial = getFormData('#form_edit_tbl_product_premium_rate_line_item');
                var data = {data : JSON.stringify(formserial)};

                $.post('/setup/save_edit_tbl_product_premium_rate_line_item?', data, function(data){
                    var result = JSON.parse(data);
                    if(result.success === true){
                        $.redirect('/setup/tbl_product_premium_rate_line_items');
                    };
                    return false;
                });
             }
        });
        $('.tbl_product_premium_rate_line_item_back').click(function(){
            $.redirect('/setup/tbl_product_premium_rate_line_items');
        });
     	"""
        title = "Edit Tbl_product_premium_rate_line_item"
        return dict(title=title, html=html, javascript=javascript)

    @expose()
    def save_new_tbl_product_premium_rate_line_item(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        if not data: return json.dumps({'success' : False})
        usernow = request.identity['user']
        this = ProductPremiumRateLineItem()
        this.product_premium_rate_id = data.get('product_premium_rate_id', None)
        this.gender_id = data.get('gender_id', None)
        this.maximum_age = data.get('maximum_age', None)
        this.minimum_age = data.get('minimum_age', None)
        this.rate_factor = data.get('rate_factor', None)
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()
        return json.dumps({'success' : True})

    @expose()
    def save_edit_tbl_product_premium_rate_line_item(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        if not data: return json.dumps({'success' : False})
        usernow = request.identity['user']
        this = self.get_tbl_product_premium_rate_line_item_by_id(**data)
        if not this: return json.dumps({'success' : False})
        this.product_premium_rate_id = data.get('product_premium_rate_id', None)
        this.gender_id = data.get('gender_id', None)
        this.maximum_age = data.get('maximum_age', None)
        this.minimum_age = data.get('minimum_age', None)
        this.rate_factor = data.get('rate_factor', None)
        if not data.get('active', None): this.active = False
        DBSession.flush()
        return json.dumps({'success' : True})

    @expose()
    def get_tbl_product_premium_rate_line_item_by_id(self, *args, **kwargs):
        return DBSession.query(ProductPremiumRateLineItem). \
            filter(ProductPremiumRateLineItem.id==kwargs.get('tbl_product_premium_rate_line_item_id', None)). \
            first()

    @expose()
    def get_active_tbl_product_premium_rate_line_item_list(self, *args, **kwargs):
        searchphrase = kwargs.get('searchphrase', None)

        tbl_product_premium_rate_line_item_product_premium_rate_id = kwargs.get('tbl_product_premium_rate_line_item_product_premium_rate_id', None)
        tbl_product_premium_rate_line_item_gender_id = kwargs.get('tbl_product_premium_rate_line_item_gender_id', None)
        maximum_age = kwargs.get('maximum_age', None)
        minimum_age = kwargs.get('minimum_age', None)
        rate_factor = kwargs.get('rate_factor', None)

        if tbl_product_premium_rate_line_item_product_premium_rate_id:
            dbase_query = DBSession.query(ProductPremiumRateLineItem). \
		    filter(ProductPremiumRateLineItem.tbl_product_premium_rate_line_item_product_premium_rate_id==tbl_product_premium_rate_line_item_product_premium_rate_id). \
                        filter(ProductPremiumRateLineItem.active==1). \
		    order_by(asc(ProductPremiumRateLineItem.tbl_product_premium_rate_line_item_id)).limit(LIMIT)
        if tbl_product_premium_rate_line_item_gender_id:
            dbase_query = DBSession.query(ProductPremiumRateLineItem). \
		    filter(ProductPremiumRateLineItem.tbl_product_premium_rate_line_item_gender_id==tbl_product_premium_rate_line_item_gender_id). \
                        filter(ProductPremiumRateLineItem.active==1). \
		    order_by(asc(ProductPremiumRateLineItem.tbl_product_premium_rate_line_item_id)).limit(LIMIT)
        if maximum_age:
            searchphrase = "%"+kwargs['maximum_age']+"%"
            dbase_query = DBSession.query(ProductPremiumRateLineItem). \
			filter(ProductPremiumRateLineItem.maximum_age.like(searchphrase)). \
                        filter(ProductPremiumRateLineItem.active==1). \
			order_by(asc(ProductPremiumRateLineItem.maximum_age)).limit(LIMIT)
        if minimum_age:
            searchphrase = "%"+kwargs['minimum_age']+"%"
            dbase_query = DBSession.query(ProductPremiumRateLineItem). \
			filter(ProductPremiumRateLineItem.minimum_age.like(searchphrase)). \
                        filter(ProductPremiumRateLineItem.active==1). \
			order_by(asc(ProductPremiumRateLineItem.minimum_age)).limit(LIMIT)
        if rate_factor:
            searchphrase = "%"+kwargs['rate_factor']+"%"
            dbase_query = DBSession.query(ProductPremiumRateLineItem). \
			filter(ProductPremiumRateLineItem.rate_factor.like(searchphrase)). \
                        filter(ProductPremiumRateLineItem.active==1). \
			order_by(asc(ProductPremiumRateLineItem.rate_factor)).limit(LIMIT)
        else:
            dbase_query = DBSession.query(ProductPremiumRateLineItem). \
                filter(ProductPremiumRateLineItem.active==1). \
                order_by(asc(ProductPremiumRateLineItem.id)). \
                limit(LIMIT)
        return dbase_query
