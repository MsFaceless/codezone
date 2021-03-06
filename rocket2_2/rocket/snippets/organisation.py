#class_name = Organisation
#table_name = tbl_organisation
#prefix =PRE
#postfix =POST
#columns_to_create = [id, name, tax_number, registration_number, financial_regulatory_number] #id - primary_key autoincrement=True
#cont_name = entity
#html_template_name = generic
#dbsession = DBSession
#controller_name = EntityController
#view_cols_list = [name, tax_number, registration_number, financial_regulatory_number]
#search_cols_list = [name, tax_number, registration_number, financial_regulatory_number]
#pdf_cols_list = [name, tax_number, registration_number, financial_regulatory_number]
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
#class_name = Organisation
#table_name =tbl_organisation
#prefix =PRE
#postfix =POST
#columns_to_create = [id, name, tax_number, registration_number, financial_regulatory_number] #id - primary_key autoincrement=True
#cont_name =entity
#html_template_name =generic
#dbsession =DBSession
#controller_name =EntityController
#view_cols_list = [name, tax_number, registration_number, financial_regulatory_number]
#search_cols_list = [name, tax_number, registration_number, financial_regulatory_number]
#pdf_cols_list = [name, tax_number, registration_number, financial_regulatory_number]
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
    def tbl_organisations(self, *args, **kwargs):
        html = self.get_active_tbl_organisation_html(*args, **kwargs)
        javascript = self.get_javascript_tbl_organisation_onload()
        title = "Tbl_organisation"
        return dict(title=title, html=html, javascript=javascript)

    @expose()
    def get_active_tbl_organisation_html(self, *args, **kwargs):
        usernow = request.identity['user']
        dbase_query = self.get_active_tbl_organisation_list(*args, **kwargs)
        outputlist = []
        for item in dbase_query:
            outputlist.append({
                'name' : "<div class='edit tbl_organisation_edit' tbl_organisation_id='{1}'>{0}</div>".format(item.name, item.id),
                'tax_number' : item.tax_number,
                'registration_number' : item.registration_number,
                'financial_regulatory_number' : item.financial_regulatory_number,
                             })
        dbcolumnlist=[
                'name',
                'tax_number',
                'registration_number',
                'financial_regulatory_number',
                    ]
        theadlist=[
                'Name',
                'Tax_Number',
                'Registration_Number',
                'Financial_Regulatory_Number',
                ]
        tbl_organisationtable = build_html_table(outputlist, dbcolumnlist, theadlist, "tbl_organisation_table")
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-6">
                            <h4 class="card-title">Tbl_organisation</h4>
                        </div>
                        <div class="col-md-6 text-right">
                            <button id="create_new_tbl_organisation" class="btn btn-primary ml-auto">Create a new Tbl_organisation</button>
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
                        {tbl_organisationtable}
                    </div>
                </div>
                </div>
            </div>
            <div id='dialogdiv'></div>
        """
        return html

    @expose()
    def get_javascript_tbl_organisation_onload(self, *args, **kwargs):
        javascript = """
        $("#create_new_tbl_organisation").click(function(){
            $('#dialogdiv').load('/entity/get_modal_new_tbl_organisation?', function(data){
                return false;
            });
        });
        $(".tbl_organisation_edit").click(function(){
            var kwargs = 'tbl_organisation_id='+$(this).attr('tbl_organisation_id');
            $('#dialogdiv').load('/entity/get_modal_edit_tbl_organisation?'+kwargs, function(data){
                return false;
            });
        });
        """
        return javascript

    @expose()
    def get_modal_new_tbl_organisation(self, *args, **kwargs):
        html = """
        <div class="modal fade" id="dialog_new_tbl_organisation" tabindex="-1" role="dialog" aria-labelledby="mytbl_organisationLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-6">
                            <h4 class="card-title">New Tbl_organisation</h4>
                        </div>
                    </div>
                    <div class="modal-body">
                        <form id='form_new_tbl_organisation'>
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
						<label class="col-md-3 col-form-label" required for="tax_number">Tax_Number</label>
						<div class="col-md-9">
							<input id="tax_number" type="text" name="tax_number" class="form-control" required='true'>
						</div>
					</div>
				</div>
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="registration_number">Registration_Number</label>
						<div class="col-md-9">
							<input id="registration_number" type="text" name="registration_number" class="form-control" required='true'>
						</div>
					</div>
				</div>
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="financial_regulatory_number">Financial_Regulatory_Number</label>
						<div class="col-md-9">
							<input id="financial_regulatory_number" type="text" name="financial_regulatory_number" class="form-control" required='true'>
						</div>
					</div>
				</div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button id='save_new_tbl_organisation' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary tbl_organisation_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
        setFormValidation('#form_new_tbl_organisation');
        $('#save_new_tbl_organisation').click(function(){
             var valid = FormIsValid("#form_new_tbl_organisation");
             if(valid){
                var formserial = getFormData('#form_new_tbl_organisation');
                var data = {data : JSON.stringify(formserial)};

                $.post('/entity/save_new_tbl_organisation?', data, function(data){
                    var result = JSON.parse(data);
                    if(result.success === true){
                        $.redirect('/entity/tbl_organisations');
                    };
                    return false;
                });
             }
        });
        $('.tbl_organisation_back').click(function(){
            $('#dialog_new_tbl_organisation').modal('hide');
        });
        $('#dialog_new_tbl_organisation').modal();
        </script>
     	"""
        return html + javascript

    @expose()
    def get_modal_edit_tbl_organisation(self, *args, **kwargs):
        tbl_organisation_id = kwargs.get('tbl_organisation_id', None)
        if not tbl_organisation_id: return ''
        this = self.get_tbl_organisation_by_id(*args, **kwargs)
        if not this: return ''
        checked = 'checked' if this.active else ''
        html = f"""
        <div class="modal fade" id="dialog_edit_tbl_organisation" tabindex="-1" role="dialog" aria-labelledby="mytbl_organisationLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-6">
                            <h4 class="card-title">New Tbl_organisation</h4>
                        </div>
                    </div>
                    <div class="modal-body">
                        <form id='form_edit_tbl_organisation'>
                            <div style='display: none' class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="tbl_organisation_id">Id</label>
						<div class="col-md-9">
							<input id="id" type="text" name="tbl_organisation_id" value="{this.id}" class="form-control" required='true'>
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
						<label class="col-md-3 col-form-label" required for="tax_number">Tax_Number</label>
						<div class="col-md-9">
							<input id="tax_number" type="text" name="tax_number" value="{this.tax_number}" class="form-control" required='true'>
						</div>
					</div>
				</div>
                            <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="registration_number">Registration_Number</label>
						<div class="col-md-9">
							<input id="registration_number" type="text" name="registration_number" value="{this.registration_number}" class="form-control" required='true'>
						</div>
					</div>
				</div>
                            <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="financial_regulatory_number">Financial_Regulatory_Number</label>
						<div class="col-md-9">
							<input id="financial_regulatory_number" type="text" name="financial_regulatory_number" value="{this.financial_regulatory_number}" class="form-control" required='true'>
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
                        <button id='save_edit_tbl_organisation' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary tbl_organisation_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
        setFormValidation('#form_edit_tbl_organisation');
        $('#save_edit_tbl_organisation').click(function(){
             var valid = FormIsValid("#form_edit_tbl_organisation");
             if(valid){
                var formserial = getFormData('#form_edit_tbl_organisation');
                var data = {data : JSON.stringify(formserial)};

                $.post('/entity/save_edit_tbl_organisation?', data, function(data){
                    var result = JSON.parse(data);
                    if(result.success === true){
                        $.redirect('/entity/tbl_organisations');
                    };
                    return false;
                });
             }
        });
        $('.tbl_organisation_back').click(function(){
            $('#dialog_edit_tbl_organisation').modal('hide');
        });
        $('#dialog_edit_tbl_organisation').modal();
        </script>
     	"""
        return html + javascript

    @expose()
    def save_new_tbl_organisation(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        if not data: return json.dumps({'success' : False, 'data' : 'No data provided'})
        usernow = request.identity['user']
        this = Organisation()
        this.name = data.get('name', None)
        this.tax_number = data.get('tax_number', None)
        this.registration_number = data.get('registration_number', None)
        this.financial_regulatory_number = data.get('financial_regulatory_number', None)
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()
        return json.dumps({'success' : True, 'data' : this.id})

    @expose()
    def save_edit_tbl_organisation(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        if not data: return json.dumps({'success' : False, 'data' : 'No data provided'})
        usernow = request.identity['user']
        this = self.get_tbl_organisation_by_id(**data)
        if not this: return json.dumps({'success' : False, 'data' : 'No tbl_organisation found for id provided'})
        this.name = data.get('name', None)
        this.tax_number = data.get('tax_number', None)
        this.registration_number = data.get('registration_number', None)
        this.financial_regulatory_number = data.get('financial_regulatory_number', None)
        if not data.get('active', None): this.active = False
        DBSession.flush()
        return json.dumps({'success' : True, 'data' : this.id})

    @expose()
    def get_tbl_organisation_by_id(self, *args, **kwargs):
        return DBSession.query(Organisation). \
            filter(Organisation.id==kwargs.get('tbl_organisation_id', None)). \
            first()

    @expose()
    def get_active_tbl_organisation_list(self, *args, **kwargs):
        searchphrase = kwargs.get('searchphrase', None)

        name = kwargs.get('name', None)
        tax_number = kwargs.get('tax_number', None)
        registration_number = kwargs.get('registration_number', None)
        financial_regulatory_number = kwargs.get('financial_regulatory_number', None)

        if name:
            searchphrase = "%"+kwargs['name']+"%"
            dbase_query = DBSession.query(Organisation). \
			filter(Organisation.name.like(searchphrase)). \
                        filter(Organisation.active==1). \
			order_by(asc(Organisation.name)).limit(LIMIT)
        if tax_number:
            searchphrase = "%"+kwargs['tax_number']+"%"
            dbase_query = DBSession.query(Organisation). \
			filter(Organisation.tax_number.like(searchphrase)). \
                        filter(Organisation.active==1). \
			order_by(asc(Organisation.tax_number)).limit(LIMIT)
        if registration_number:
            searchphrase = "%"+kwargs['registration_number']+"%"
            dbase_query = DBSession.query(Organisation). \
			filter(Organisation.registration_number.like(searchphrase)). \
                        filter(Organisation.active==1). \
			order_by(asc(Organisation.registration_number)).limit(LIMIT)
        if financial_regulatory_number:
            searchphrase = "%"+kwargs['financial_regulatory_number']+"%"
            dbase_query = DBSession.query(Organisation). \
			filter(Organisation.financial_regulatory_number.like(searchphrase)). \
                        filter(Organisation.active==1). \
			order_by(asc(Organisation.financial_regulatory_number)).limit(LIMIT)
        else:
            dbase_query = DBSession.query(Organisation). \
                filter(Organisation.active==1). \
                order_by(asc(Organisation.id)). \
                limit(LIMIT)
        return dbase_query
