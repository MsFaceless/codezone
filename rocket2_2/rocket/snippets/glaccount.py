#class_name = GeneralLedgerAccount
#table_name = tbl_general_ledger_account
#prefix =PRE
#postfix =POST
#columns_to_create = [id,name,debit_account,credit_account,gl_key] #id - primary_key autoincrement=True
#cont_name = product
#html_template_name = generic
#dbsession = DBSession
#controller_name = ProductController
#view_cols_list = [name,debit_account,credit_account,gl_key]
#search_cols_list = [name,debit_account,credit_account,gl_key]
#pdf_cols_list = [name,debit_account,credit_account,gl_key]
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
#class_name = GeneralLedgerAccount
#table_name =tbl_general_ledger_account
#prefix =PRE
#postfix =POST
#columns_to_create = [id,name,debit_account,credit_account,gl_key] #id - primary_key autoincrement=True
#cont_name =product
#html_template_name =generic
#dbsession =DBSession
#controller_name =ProductController
#view_cols_list = [name,debit_account,credit_account,gl_key]
#search_cols_list = [name,debit_account,credit_account,gl_key]
#pdf_cols_list = [name,debit_account,credit_account,gl_key]
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
    def tbl_general_ledger_accounts(self, *args, **kwargs):
        html = self.get_active_tbl_general_ledger_account_html(*args, **kwargs)
        javascript = self.get_javascript_tbl_general_ledger_account_onload()
        title = "Tbl_general_ledger_account"
        return dict(title=title, html=html, javascript=javascript)

    @expose()
    def get_active_tbl_general_ledger_account_html(self, *args, **kwargs):
        usernow = request.identity['user']
        dbase_query = self.get_active_tbl_general_ledger_account_list(*args, **kwargs)
        outputlist = []
        for item in dbase_query:
            outputlist.append({ 
                'name' : "<div class='edit tbl_general_ledger_account_edit' tbl_general_ledger_account_id='{1}'>{0}</div>".format(item.name, item.id),  
                'debit_account' : item.debit_account, 
                'credit_account' : item.credit_account, 
                'gl_key' : item.gl_key, 
                             })
        dbcolumnlist=[ 
                'name', 
                'debit_account', 
                'credit_account', 
                'gl_key', 
                    ]
        theadlist=[ 
                'Name', 
                'Debit_Account', 
                'Credit_Account', 
                'Gl_Key', 
                ]
        tbl_general_ledger_accounttable = build_html_table(outputlist, dbcolumnlist, theadlist, "tbl_general_ledger_account_table")
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-6">
                            <h4 class="card-title">Tbl_general_ledger_account</h4>
                        </div>
                        <div class="col-md-6 text-right">
                            <button id="create_new_tbl_general_ledger_account" class="btn btn-primary ml-auto">Create a new Tbl_general_ledger_account</button>
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
                        {tbl_general_ledger_accounttable}
                    </div>
                </div>
                </div>
            </div>
            <div id='dialogdiv'></div>
        """
        return html

    @expose()
    def get_javascript_tbl_general_ledger_account_onload(self, *args, **kwargs):
        javascript = """
        $("#create_new_tbl_general_ledger_account").click(function(){
            $('#dialogdiv').load('/product/get_modal_new_tbl_general_ledger_account?', function(data){
                return false;
            });
        });
        $(".tbl_general_ledger_account_edit").click(function(){
            var kwargs = 'tbl_general_ledger_account_id='+$(this).attr('tbl_general_ledger_account_id');
            $('#dialogdiv').load('/product/get_modal_edit_tbl_general_ledger_account?'+kwargs, function(data){
                return false;
            });
        });
        """
        return javascript

    @expose()
    def get_modal_new_tbl_general_ledger_account(self, *args, **kwargs):
        html = """
        <div class="modal fade" id="dialog_new_tbl_general_ledger_account" tabindex="-1" role="dialog" aria-labelledby="mytbl_general_ledger_accountLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-6">
                            <h4 class="card-title">New Tbl_general_ledger_account</h4>
                        </div>
                    </div>
                    <div class="modal-body">
                        <form id='form_new_tbl_general_ledger_account'> 
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
						<label class="col-md-3 col-form-label" required for="debit_account">Debit_Account</label>
						<div class="col-md-9">
							<input id="debit_account" type="text" name="debit_account" class="form-control" required='true'>
						</div>
					</div>
				</div>
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="credit_account">Credit_Account</label>
						<div class="col-md-9">
							<input id="credit_account" type="text" name="credit_account" class="form-control" required='true'>
						</div>
					</div>
				</div>
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="gl_key">Gl_Key</label>
						<div class="col-md-9">
							<input id="gl_key" type="text" name="gl_key" class="form-control" required='true'>
						</div>
					</div>
				</div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button id='save_new_tbl_general_ledger_account' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary tbl_general_ledger_account_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
        setFormValidation('#form_new_tbl_general_ledger_account'); 
        $('#save_new_tbl_general_ledger_account').click(function(){
             var valid = FormIsValid("#form_new_tbl_general_ledger_account");
             if(valid){
                var formserial = getFormData('#form_new_tbl_general_ledger_account');
                var data = {data : JSON.stringify(formserial)};

                $.post('/product/save_new_tbl_general_ledger_account?', data, function(data){
                    var result = JSON.parse(data);
                    if(result.success === true){
                        $.redirect('/product/tbl_general_ledger_accounts');
                    };
                    return false;
                });
             }
        });
        $('.tbl_general_ledger_account_back').click(function(){
            $('#dialog_new_tbl_general_ledger_account').modal('hide');
        });
        $('#dialog_new_tbl_general_ledger_account').modal();
        </script>
     	"""
        return html + javascript

    @expose()
    def get_modal_edit_tbl_general_ledger_account(self, *args, **kwargs):
        tbl_general_ledger_account_id = kwargs.get('tbl_general_ledger_account_id', None)
        if not tbl_general_ledger_account_id: return ''
        this = self.get_tbl_general_ledger_account_by_id(*args, **kwargs)
        if not this: return ''
        checked = 'checked' if this.active else ''
        html = f"""
        <div class="modal fade" id="dialog_edit_tbl_general_ledger_account" tabindex="-1" role="dialog" aria-labelledby="mytbl_general_ledger_accountLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-6">
                            <h4 class="card-title">New Tbl_general_ledger_account</h4>
                        </div>
                    </div>
                    <div class="modal-body">
                        <form id='form_edit_tbl_general_ledger_account'> 
                            <div style='display:none' class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="tbl_general_ledger_account_id">Id</label>
						<div class="col-md-9">
							<input id="id" type="text" name="tbl_general_ledger_account_id" value="{this.id}" class="form-control" required='true'>
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
						<label class="col-md-3 col-form-label" required for="debit_account">Debit_Account</label>
						<div class="col-md-9">
							<input id="debit_account" type="text" name="debit_account" value="{this.debit_account}" class="form-control" required='true'>
						</div>
					</div>
				</div>
                            <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="credit_account">Credit_Account</label>
						<div class="col-md-9">
							<input id="credit_account" type="text" name="credit_account" value="{this.credit_account}" class="form-control" required='true'>
						</div>
					</div>
				</div>
                            <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="gl_key">Gl_Key</label>
						<div class="col-md-9">
							<input id="gl_key" type="text" name="gl_key" value="{this.gl_key}" class="form-control" required='true'>
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
                        <button id='save_edit_tbl_general_ledger_account' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary tbl_general_ledger_account_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
        setFormValidation('#form_edit_tbl_general_ledger_account'); 
        $('#save_edit_tbl_general_ledger_account').click(function(){
             var valid = FormIsValid("#form_edit_tbl_general_ledger_account");
             if(valid){
                var formserial = getFormData('#form_edit_tbl_general_ledger_account');
                var data = {data : JSON.stringify(formserial)};

                $.post('/product/save_edit_tbl_general_ledger_account?', data, function(data){
                    var result = JSON.parse(data);
                    if(result.success === true){
                        $.redirect('/product/tbl_general_ledger_accounts');
                    };
                    return false;
                });
             }
        });
        $('.tbl_general_ledger_account_back').click(function(){
            $('#dialog_edit_tbl_general_ledger_account').modal('hide');
        });
        $('#dialog_edit_tbl_general_ledger_account').modal();
        </script>
     	"""
        return html + javascript

    @expose()
    def save_new_tbl_general_ledger_account(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        if not data: return json.dumps({'success' : False, 'data' : 'No data provided'})
        usernow = request.identity['user']
        this = GeneralLedgerAccount()
        this.name = data.get('name', None)
        this.debit_account = data.get('debit_account', None)
        this.credit_account = data.get('credit_account', None)
        this.gl_key = data.get('gl_key', None)
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()
        return json.dumps({'success' : True, 'data' : this.id})

    @expose()
    def save_edit_tbl_general_ledger_account(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        if not data: return json.dumps({'success' : False, 'data' : 'No data provided'})
        usernow = request.identity['user']
        this = self.get_tbl_general_ledger_account_by_id(**data)
        if not this: return json.dumps({'success' : False, 'data' : 'No tbl_general_ledger_account found for id provided'}) 
        this.name = data.get('name', None)
        this.debit_account = data.get('debit_account', None)
        this.credit_account = data.get('credit_account', None)
        this.gl_key = data.get('gl_key', None)
        if not data.get('active', None): this.active = False
        DBSession.flush()
        return json.dumps({'success' : True, 'data' : this.id})

    @expose()
    def get_tbl_general_ledger_account_by_id(self, *args, **kwargs):
        return DBSession.query(GeneralLedgerAccount). \
            filter(GeneralLedgerAccount.id==kwargs.get('tbl_general_ledger_account_id', None)). \
            first()

    @expose()
    def get_active_tbl_general_ledger_account_list(self, *args, **kwargs):
        searchphrase = kwargs.get('searchphrase', None)

        name = kwargs.get('name', None)
        debit_account = kwargs.get('debit_account', None)
        credit_account = kwargs.get('credit_account', None)
        gl_key = kwargs.get('gl_key', None)

        if name:
            searchphrase = "%"+kwargs['name']+"%" 
            dbase_query = DBSession.query(GeneralLedgerAccount). \
			filter(GeneralLedgerAccount.name.like(searchphrase)). \
                        filter(GeneralLedgerAccount.active==1). \
			order_by(asc(GeneralLedgerAccount.name)).limit(LIMIT)
        if debit_account:
            searchphrase = "%"+kwargs['debit_account']+"%" 
            dbase_query = DBSession.query(GeneralLedgerAccount). \
			filter(GeneralLedgerAccount.debit_account.like(searchphrase)). \
                        filter(GeneralLedgerAccount.active==1). \
			order_by(asc(GeneralLedgerAccount.debit_account)).limit(LIMIT)
        if credit_account:
            searchphrase = "%"+kwargs['credit_account']+"%" 
            dbase_query = DBSession.query(GeneralLedgerAccount). \
			filter(GeneralLedgerAccount.credit_account.like(searchphrase)). \
                        filter(GeneralLedgerAccount.active==1). \
			order_by(asc(GeneralLedgerAccount.credit_account)).limit(LIMIT)
        if gl_key:
            searchphrase = "%"+kwargs['gl_key']+"%" 
            dbase_query = DBSession.query(GeneralLedgerAccount). \
			filter(GeneralLedgerAccount.gl_key.like(searchphrase)). \
                        filter(GeneralLedgerAccount.active==1). \
			order_by(asc(GeneralLedgerAccount.gl_key)).limit(LIMIT)
        else:
            dbase_query = DBSession.query(GeneralLedgerAccount). \
                filter(GeneralLedgerAccount.active==1). \
                order_by(asc(GeneralLedgerAccount.id)). \
                limit(LIMIT)
        return dbase_query
