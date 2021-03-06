#class_name = PolicyBenefitEmployeeAssetTemp
#table_name = policy_benefit_employee_asset_temp
#prefix =shortname
#postfix =POST
#columns_to_create = [id, policy_benefit_id, product_benefit_id, name, surname] #id - primary_key autoincrement=True
#cont_name = product
#html_template_name = generic
#dbsession = DBSession
#controller_name = ProductController
#view_cols_list = [name, surname]
#search_cols_list = [name, surname]
#pdf_cols_list = [name, surname]
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
#class_name = PolicyBenefitEmployeeAssetTemp
#table_name =policy_benefit_employee_asset_temp
#prefix =shortname
#postfix =POST
#columns_to_create = [id, policy_benefit_id, product_benefit_id, name, surname] #id - primary_key autoincrement=True
#cont_name =product
#html_template_name =generic
#dbsession =DBSession
#controller_name =ProductController
#view_cols_list = [name, surname]
#search_cols_list = [name, surname]
#pdf_cols_list = [name, surname]
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
    def policy_benefit_employee_asset_temps(self, *args, **kwargs):
        html = self.get_active_policy_benefit_employee_asset_temp_html(*args, **kwargs)
        javascript = self.get_javascript_policy_benefit_employee_asset_temp_onload()
        title = "Policy_benefit_employee_asset_temp"
        return dict(title=title, html=html, javascript=javascript)

    @expose()
    def get_active_policy_benefit_employee_asset_temp_html(self, *args, **kwargs):
        dbase_query = PolicyBenefitEmployeeAssetTemp.get_all('id')
        outputlist = []
        for item in dbase_query:
            outputlist.append({ 
                'name' : "<div class='edit policy_benefit_employee_asset_temp_edit' policy_benefit_employee_asset_temp_id='{1}'>{0}</div>".format(item.name, item.id),  
                'surname' : item.surname, 
                             })
        dbcolumnlist=[ 
                'name', 
                'surname', 
                    ]
        theadlist=[ 
                'Name', 
                ' Surname', 
                ]
        htmltbl = build_html_table(outputlist, dbcolumnlist, theadlist, "policy_benefit_employee_asset_temp_table")
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-6">
                            <h4 class="card-title">Policy_benefit_employee_asset_temp</h4>
                        </div>
                        <div class="col-md-6 text-right">
                            <button id="create_new_policy_benefit_employee_asset_temp" class="btn btn-primary ml-auto">Create New Policy_benefit_employee_asset_temp</button>
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
                        {htmltbl}
                    </div>
                </div>
                </div>
            </div>
        </div>
        """
        return html

    @expose()
    def get_javascript_policy_benefit_employee_asset_temp_onload(self, *args, **kwargs):
        javascript = """
        $("#create_new_policy_benefit_employee_asset_temp").click(function(){
            $('#dialogdiv').load('/product/get_modal_policy_benefit_employee_asset_temp?', function(data){
                return false;
            });
        });
        $(".policy_benefit_employee_asset_temp_edit").click(function(){
            var kwargs = 'policy_benefit_employee_asset_temp_id='+$(this).attr('policy_benefit_employee_asset_temp_id');
            $('#dialogdiv').load('/product/get_modal_policy_benefit_employee_asset_temp?', kwargs, function(data){
                return false;
            });
        });
        """
        return javascript

    @expose()
    def get_modal_policy_benefit_employee_asset_temp(self, *args, **kwargs):
        policy_benefit_employee_asset_temp_id = kwargs.get('policy_benefit_employee_asset_temp_id', None)
        policy_benefit_employee_asset_temp = None
        hidden_input = ''
        if policy_benefit_employee_asset_temp_id:
            policy_benefit_employee_asset_temp = PolicyBenefitEmployeeAssetTemp.by_id(policy_benefit_employee_asset_temp)
            hidden_input = get_hidden_input(**{'id': 'policy_benefit_employee_asset_temp_id', 'value': policy_benefit_employee_asset_temp_id}) 
        name = name if policy_benefit_employee_asset_temp else '' 
        surname = surname if policy_benefit_employee_asset_temp else '' 
        html = f"""
        <div class="modal fade" id="dialog_policy_benefit_employee_asset_temp" tabindex="-1" role="dialog" aria-labelledby="mypolicy_benefit_employee_asset_tempLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-6">
                            <h4 class="card-title">New Policy_benefit_employee_asset_temp</h4>
                        </div>
                    </div>
                    <div class="modal-body">
                        <form id='form_new_policy_benefit_employee_asset_temp'> 
                        {hidden_input}
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="name">Name</label>
						<div class="col-md-9">
							<input id="name" value="{name}" type="text" name="name" class="form-control" required='true'>
						</div>
					</div>
				</div>
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="surname"> Surname</label>
						<div class="col-md-9">
							<input id="surname" value="{surname}" type="text" name="surname" class="form-control" required='true'>
						</div>
					</div>
				</div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button id='save_policy_benefit_employee_asset_temp' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary policy_benefit_employee_asset_temp_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
        var form_id = '#form_policy_benefit_employee_asset_temp'
        setFormValidation(form_id); 
        $('#save_policy_benefit_employee_asset_temp').click(function(){
             var valid = FormIsValid(form_id);
             if(valid){
                var formserial = $(form_id).serialize();
                $.post('/product/save_policy_benefit_employee_asset_temp?', formserial, function(data){
                    $.redirect('/product/policy_benefit_employee_asset_temps');
                    return false;
                });
             }
        });
        $('.policy_benefit_employee_asset_temp_back').click(function(){
            $('#dialog_policy_benefit_employee_asset_temp').modal('hide');
        });
        $('#dialog_policy_benefit_employee_asset_temp').modal();
        </script>
     	"""
        return html + javascript

    @expose()
    def save_policy_benefit_employee_asset_temp(self, *args, **kwargs):
        usernow = request.identity.get('user', None)
        policy_benefit_employee_asset_temp_id = kwargs.get('policy_benefit_employee_asset_temp_id', None)
        if not policy_benefit_employee_asset_temp_id:
            this = PolicyBenefitEmployeeAssetTemp()
            this.policy_benefit_id = kwargs.get('policy_benefit_id', None)
            this.product_benefit_id = kwargs.get('product_benefit_id', None)
            this.name = kwargs.get('name', None)
            this.surname = kwargs.get('surname', None)
            this.added_by = usernow.id
            DBSession.add(this)
            DBSession.flush()
        else:
            this = PolicyBenefitEmployeeAssetTemp.by_id(policy_benefit_employee_asset_temp_id) 
            if not this: return 'false'
            this.policy_benefit_id = kwargs.get('policy_benefit_id', None)
            this.product_benefit_id = kwargs.get('product_benefit_id', None)
            this.name = kwargs.get('name', None)
            this.surname = kwargs.get('surname', None)
            DBSession.flush()
        return str(this.id)
