# class_name = Bank
# table_name = bank
# prefix =PRE
# postfix =POST
# columns_to_create = [id, name] #id - primary_key autoincrement=True
# cont_name = setup
# html_template_name = generic
# dbsession = DBSession
# controller_name = SetupController
# view_cols_list = [name]
# search_cols_list = [name]
# pdf_cols_list = [name]
# link_to_id_or_None = None
# link_class_name_None = None
"""
@q: 1ggf=wv$h"ay 2ggf=wv$h"by 3ggf=wv$h"cy 4ggf=wv$h"dy 5ggf[wvt]"ey 6ggf=wv$h"fy 7ggf=wv$h"gy 8ggf=wv$h"hy 9ggf=wv$h"iy 10ggf[wvt]"jy 11ggf[wvt]"ky 12ggf[wvt]"ly
@w: "api "bgpi "cgp i "dgp i "egpi "fgp i "ggp i "hgp i "igp i "jpi "kpi "lpi
@t: 23ggVGd22ggo_tgcreateclas
@r: 16ggf:wv$"qy 17ggf:wv$"wy 18ggf:wv$"ty @q@t
Instructions: run @r then complete the snip with <ctr-l> then <escape> then @w
"""


##################################################################################################################
# class_name = Bank
# table_name =bank
# prefix =PRE
# postfix =POST
# columns_to_create = [id, name] #id - primary_key autoincrement=True
# cont_name =setup
# html_template_name =generic
# dbsession =DBSession
# controller_name =SetupController
# view_cols_list = [name]
# search_cols_list = [name]
# pdf_cols_list = [name]
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
    @expose('rocket_app.templates.generic')
    def banks(self, *args, **kwargs):
        html = self.get_active_bank_html(*args, **kwargs)
        javascript = self.get_javascript_bank_onload()
        title = "Bank"
        return dict(title=title, html=html, javascript=javascript)

    @expose()
    def get_active_bank_html(self, *args, **kwargs):
        usernow = request.identity['user']
        dbase_query = self.get_active_bank_list(*args, **kwargs)
        outputlist = []
        for item in dbase_query:
            outputlist.append({
                'name': "<div class='edit bank_edit' bank_id='{1}'>{0}</div>".format(item.name, item.id),
            })
        dbcolumnlist = [
            'name',
        ]
        theadlist = [
            'Name',
        ]
        banktable = build_html_table(outputlist, dbcolumnlist, theadlist, "bank_table")
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-6">
                            <h4 class="card-title">Bank</h4>
                        </div>
                        <div class="col-md-6 text-right">
                            <button id="create_new_bank" class="btn btn-primary ml-auto">Create a New Bank</button>
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
                        {banktable}
                    </div>
                </div>
                </div>
            </div>
            <div id='dialogdiv'></div>
        """
        return html

    @expose()
    def get_javascript_bank_onload(self, *args, **kwargs):
        javascript = """
        $("#create_new_bank").click(function(){
            $('#dialogdiv').load('/setup/get_modal_new_bank?', function(data){
                return false;
            });
        });
        $(".bank_edit").click(function(){
            var kwargs = 'bank_id='+$(this).attr('bank_id');
            $('#dialogdiv').load('/setup/get_modal_edit_bank?'+kwargs, function(data){
                return false;
            });
        });
        """
        return javascript

    @expose()
    def get_modal_new_bank(self, *args, **kwargs):
        html = """
        <div class="modal fade" id="dialog_new_bank" tabindex="-1" role="dialog" aria-labelledby="mybankLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-6">
                            <h4 class="card-title">New Bank</h4>
                        </div>
                    </div>
                    <div class="modal-body">
                        <form id='form_new_bank'>
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
                        <button id='save_new_bank' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary bank_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
        setFormValidation('#form_new_bank');
        $('#save_new_bank').click(function(){
             var valid = FormIsValid("#form_new_bank");
             if(valid){
                var formserial = getFormData('#form_new_bank');
                var data = {data : JSON.stringify(formserial)};

                $.post('/setup/save_new_bank?', data, function(data){
                    var result = JSON.parse(data);
                    if(result.success === true){
                        $.redirect('/setup/banks');
                    };
                    return false;
                });
             }
        });
        $('.bank_back').click(function(){
            $('#dialog_new_bank').modal('hide');
        });
        $('#dialog_new_bank').modal();
        </script>
     	"""
        return html + javascript

    @expose()
    def get_modal_edit_bank(self, *args, **kwargs):
        bank_id = kwargs.get('bank_id', None)
        if not bank_id: return ''
        this = self.get_bank_by_id(*args, **kwargs)
        if not this: return ''
        checked = 'checked' if this.active else ''
        html = f"""
        <div class="modal fade" id="dialog_edit_bank" tabindex="-1" role="dialog" aria-labelledby="mybankLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-6">
                            <h4 class="card-title">New Bank</h4>
                        </div>
                    </div>
                    <div class="modal-body">
                        <form id='form_edit_bank'>
                            <div style='display:none' class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="bank_id">Id</label>
						<div class="col-md-9">
							<input id="id" type="text" name="bank_id" value="{this.id}" class="form-control" required='true'>
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
                            <div class="form-group row">
                              <label class="col-4 col-form-label" for="active" required>Active</label>
                              <div class="col-8"><div class="form-check">
                                <input class="form-check-input" type="checkbox" name="active" id="active" {checked}/></div>
                              </div>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button id='save_edit_bank' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary bank_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
        setFormValidation('#form_edit_bank');
        $('#save_edit_bank').click(function(){
             var valid = FormIsValid("#form_edit_bank");
             if(valid){
                var formserial = getFormData('#form_edit_bank');
                var data = {data : JSON.stringify(formserial)};

                $.post('/setup/save_edit_bank?', data, function(data){
                    var result = JSON.parse(data);
                    if(result.success === true){
                        $.redirect('/setup/banks');
                    };
                    return false;
                });
             }
        });
        $('.bank_back').click(function(){
            $('#dialog_edit_bank').modal('hide');
        });
        $('#dialog_edit_bank').modal();
        </script>
     	"""
        return html + javascript

    @expose()
    def save_new_bank(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        if not data: return json.dumps({'success': False, 'data': 'No data provided'})
        usernow = request.identity['user']
        this = Bank()
        this.name = data.get('name', None)
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()
        return json.dumps({'success': True, 'data': this.id})

    @expose()
    def save_edit_bank(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        if not data: return json.dumps({'success': False, 'data': 'No data provided'})
        usernow = request.identity['user']
        this = self.get_bank_by_id(**data)
        if not this: return json.dumps({'success': False, 'data': 'No bank found for id provided'})
        this.name = data.get('name', None)
        if not data.get('active', None): this.active = False
        DBSession.flush()
        return json.dumps({'success': True, 'data': this.id})

    @expose()
    def get_bank_by_id(self, *args, **kwargs):
        return DBSession.query(Bank). \
            filter(Bank.id == kwargs.get('bank_id', None)). \
            first()

    @expose()
    def get_active_bank_list(self, *args, **kwargs):
        searchphrase = kwargs.get('searchphrase', None)

        name = kwargs.get('name', None)

        if name:
            searchphrase = "%" + kwargs['name'] + "%"
            dbase_query = DBSession.query(Bank). \
                filter(Bank.name.like(searchphrase)). \
                filter(Bank.active == 1). \
                order_by(asc(Bank.name)).limit(LIMIT)
        else:
            dbase_query = DBSession.query(Bank). \
                filter(Bank.active == 1). \
                order_by(asc(Bank.id)). \
                limit(LIMIT)
        return dbase_query
