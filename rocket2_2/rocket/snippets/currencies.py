# class_name = Currency
# table_name = currency
# prefix =PRE
# postfix =POST
# columns_to_create = [id, code, name, home_currency] #id - primary_key autoincrement=True
# cont_name = setup
# html_template_name = generic
# dbsession = DBSession
# controller_name = SetupController
# view_cols_list = [code, name, home_currency]
# search_cols_list = [code, name, home_currency]
# pdf_cols_list = [code, name, home_currency]
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
# class_name = Currency
# table_name =currency
# prefix =PRE
# postfix =POST
# columns_to_create = [id, code, name, home_currency] #id - primary_key autoincrement=True
# cont_name =setup
# html_template_name =generic
# dbsession =DBSession
# controller_name =SetupController
# view_cols_list = [code, name, home_currency]
# search_cols_list = [code, name, home_currency]
# pdf_cols_list = [code, name, home_currency]
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
    def currencies(self, *args, **kwargs):
        html = self.get_active_currency_html(*args, **kwargs)
        javascript = self.get_javascript_currency_onload()
        title = "Currency"
        return dict(title=title, html=html, javascript=javascript)

    @expose()
    def get_active_currency_html(self, *args, **kwargs):
        usernow = request.identity['user']
        dbase_query = self.get_active_currency_list(*args, **kwargs)
        outputlist = []
        for item in dbase_query:
            outputlist.append({
                'code': "<div class='edit currency_edit' currency_id='{1}'>{0}</div>".format(item.code,
                                                                                                     item.id),
                'name': item.name,
                'home_currency': item.home_currency,
            })
        dbcolumnlist = [
            'code',
            'name',
            'home_currency',
        ]
        theadlist = [
            'Code',
            ' Name',
            ' Home_Currency',
        ]
        currencytable = build_html_table(outputlist, dbcolumnlist, theadlist, "currency_table")
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-6">
                            <h4 class="card-title">Currency</h4>
                        </div>
                        <div class="col-md-6 text-right">
                            <button id="create_new_currency" class="btn btn-primary ml-auto">Create a New Currency</button>
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
                        {currencytable}
                    </div>
                </div>
                </div>
            </div>
            <div id='dialogdiv'></div>
        """
        return html

    @expose()
    def get_javascript_currency_onload(self, *args, **kwargs):
        javascript = """
        $("#create_new_currency").click(function(){
            $('#dialogdiv').load('/setup/get_modal_new_currency?', function(data){
                return false;
            });
        });
        $(".currency_edit").click(function(){
            var kwargs = 'currency_id='+$(this).attr('currency_id');
            $('#dialogdiv').load('/setup/get_modal_edit_currency?'+kwargs, function(data){
                return false;
            });
        });
        """
        return javascript

    @expose()
    def get_modal_new_currency(self, *args, **kwargs):
        html = """
        <div class="modal fade" id="dialog_new_currency" tabindex="-1" role="dialog" aria-labelledby="mycurrencyLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-6">
                            <h4 class="card-title">New Currency</h4>
                        </div>
                    </div>
                    <div class="modal-body">
                        <form id='form_new_currency'>
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
						<label class="col-md-3 col-form-label" required for="name"> Name</label>
						<div class="col-md-9">
							<input id="name" type="text" name="name" class="form-control" required='true'>
						</div>
					</div>
				</div>
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="home_currency"> Home_Currency</label>
						<div class="col-md-9">
							<input id="home_currency" type="text" name="home_currency" class="form-control" required='true'>
						</div>
					</div>
				</div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button id='save_new_currency' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary currency_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
        setFormValidation('#form_new_currency');
        $('#save_new_currency').click(function(){
             var valid = FormIsValid("#form_new_currency");
             if(valid){
                var formserial = getFormData('#form_new_currency');
                var data = {data : JSON.stringify(formserial)};

                $.post('/setup/save_new_currency?', data, function(data){
                    var result = JSON.parse(data);
                    if(result.success === true){
                        $.redirect('/setup/currencies');
                    };
                    return false;
                });
             }
        });
        $('.currency_back').click(function(){
            $('#dialog_new_currency').modal('hide');
        });
        $('#dialog_new_currency').modal();
        </script>
     	"""
        return html + javascript

    @expose()
    def get_modal_edit_currency(self, *args, **kwargs):
        currency_id = kwargs.get('currency_id', None)
        if not currency_id: return ''
        this = self.get_currency_by_id(*args, **kwargs)
        if not this: return ''
        checked = 'checked' if this.active else ''
        html = f"""
        <div class="modal fade" id="dialog_edit_currency" tabindex="-1" role="dialog" aria-labelledby="mycurrencyLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-6">
                            <h4 class="card-title">Edit Currency</h4>
                        </div>
                    </div>
                    <div class="modal-body">
                        <form id='form_edit_currency'>
                            <div style='display:none' class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="currency_id">Id</label>
						<div class="col-md-9">
							<input id="id" type="text" name="currency_id" value="{this.id}" class="form-control" required='true'>
						</div>
					</div>
				</div>
                            <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="code"> Code</label>
						<div class="col-md-9">
							<input id="code" type="text" name="code" value="{this.code}" class="form-control" required='true'>
						</div>
					</div>
				</div>
                            <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="name"> Name</label>
						<div class="col-md-9">
							<input id="name" type="text" name="name" value="{this.name}" class="form-control" required='true'>
						</div>
					</div>
				</div>
                            <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="home_currency"> Home_Currency</label>
						<div class="col-md-9">
							<input id="home_currency" type="text" name="home_currency" value="{this.home_currency}" class="form-control" required='true'>
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
                        <button id='save_edit_currency' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary currency_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
        setFormValidation('#form_edit_currency');
        $('#save_edit_currency').click(function(){
             var valid = FormIsValid("#form_edit_currency");
             if(valid){
                var formserial = getFormData('#form_edit_currency');
                var data = {data : JSON.stringify(formserial)};

                $.post('/setup/save_edit_currency?', data, function(data){
                    var result = JSON.parse(data);
                    if(result.success === true){
                        $.redirect('/setup/currencies');
                    };
                    return false;
                });
             }
        });
        $('.currency_back').click(function(){
            $('#dialog_edit_currency').modal('hide');
        });
        $('#dialog_edit_currency').modal();
        </script>
     	"""
        return html + javascript

    @expose()
    def save_new_currency(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        if not data: return json.dumps({'success': False, 'data': 'No data provided'})
        usernow = request.identity['user']
        this = Currency()
        this.code = data.get('code', None)
        this.name = data.get('name', None)
        this.home_currency = data.get('home_currency', None)
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()
        return json.dumps({'success': True, 'data': this.id})

    @expose()
    def save_edit_currency(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        if not data: return json.dumps({'success': False, 'data': 'No data provided'})
        usernow = request.identity['user']
        this = self.get_currency_by_id(**data)
        if not this: return json.dumps({'success': False, 'data': 'No currency found for id provided'})
        this.code = data.get('code', None)
        this.name = data.get('name', None)
        this.home_currency = data.get('home_currency', None)
        if not data.get('active', None): this.active = False
        DBSession.flush()
        return json.dumps({'success': True, 'data': this.id})

    @expose()
    def get_currency_by_id(self, *args, **kwargs):
        return DBSession.query(Currency). \
            filter(Currency.id == kwargs.get('currency_id', None)). \
            first()

    @expose()
    def get_active_currency_list(self, *args, **kwargs):
        searchphrase = kwargs.get('searchphrase', None)

        code = kwargs.get('code', None)
        name = kwargs.get('name', None)
        home_currency = kwargs.get('home_currency', None)

        if code:
            searchphrase = "%" + kwargs['code'] + "%"
            dbase_query = DBSession.query(Currency). \
                filter(Currency.code.like(searchphrase)). \
                filter(Currency.active == 1). \
                order_by(asc(Currency.code)).limit(LIMIT)
        if name:
            searchphrase = "%" + kwargs['name'] + "%"
            dbase_query = DBSession.query(Currency). \
                filter(Currency.name.like(searchphrase)). \
                filter(Currency.active == 1). \
                order_by(asc(Currency.name)).limit(LIMIT)
        if home_currency:
            searchphrase = "%" + kwargs['home_currency'] + "%"
            dbase_query = DBSession.query(Currency). \
                filter(Currency.home_currency.like(searchphrase)). \
                filter(Currency.active == 1). \
                order_by(asc(Currency.home_currency)).limit(LIMIT)
        else:
            dbase_query = DBSession.query(Currency). \
                filter(Currency.active == 1). \
                order_by(asc(Currency.id)). \
                limit(LIMIT)
        return dbase_query
