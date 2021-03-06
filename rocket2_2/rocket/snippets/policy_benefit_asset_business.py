#class_name = PolicyBenefitBusinessAssetTemp
#table_name = policy_benefit_business_asset_temp
#prefix =PRE
#postfix =POST
#columns_to_create = [id, policy_benefit_id, product_benefit_id, company_registration_number, turnover, email, contact_name, contact_number, activity] #id - primary_key autoincrement=True
#cont_name =policy
#html_template_name = generic
#dbsession = DBSession
#controller_name = PolicyController
#view_cols_list = [company_registration_number, turnover, email, contact_name, contact_number, activity]
#search_cols_list = [company_registration_number, turnover, email, contact_name, contact_number, activity]
#pdf_cols_list = [company_registration_number, turnover, email, contact_name, contact_number, activity]
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
#class_name = PolicyBenefitBusinessAssetTemp
#table_name =policy_benefit_business_asset_temp
#prefix =PRE
#postfix =POST
#columns_to_create = [id, policy_benefit_id, product_benefit_id, company_registration_number, turnover, email, contact_name, contact_number, activity] #id - primary_key autoincrement=True
#cont_name =policy
#html_template_name =generic
#dbsession =DBSession
#controller_name =PolicyController
#view_cols_list = [company_registration_number, turnover, email, contact_name, contact_number, activity]
#search_cols_list = [company_registration_number, turnover, email, contact_name, contact_number, activity]
#pdf_cols_list = [company_registration_number, turnover, email, contact_name, contact_number, activity]
#link_to_id_or_None =
#link_class_name_None =

############################
# Controller
############################


class PolicyController(BaseController):
    """Docstring for policy ."""

    def __init__(self, *args, **kwargs):
        pass

    @require(predicates.not_anonymous())
    @expose('rocket_app.templates.generic')
    def policy_benefit_business_asset_temps(self, *args, **kwargs):
        html = self.get_active_policy_benefit_business_asset_temp_html(*args, **kwargs)
        javascript = self.get_javascript_policy_benefit_business_asset_temp_onload()
        title = "Policy_benefit_business_asset_temp"
        return dict(title=title, html=html, javascript=javascript)

    @expose()
    def get_active_policy_benefit_business_asset_temp_html(self, *args, **kwargs):
        dbase_query = PolicyBenefitBusinessAssetTemp.get_all('id')
        outputlist = []
        for item in dbase_query:
            outputlist.append({
                'company_registration_number' : "<div class='edit policy_benefit_business_asset_temp_edit' policy_benefit_business_asset_temp_id='{1}'>{0}</div>".format(item.company_registration_number, item.id),
                'turnover' : item.turnover,
                'email' : item.email,
                'contact_name' : item.contact_name,
                'contact_number' : item.contact_number,
                'activity' : item.activity,
                             })
        dbcolumnlist=[
                'company_registration_number',
                'turnover',
                'email',
                'contact_name',
                'contact_number',
                'activity',
                    ]
        theadlist=[
                'Company_Registration_Number',
                'Turnover',
                'Email',
                'Contact_Name',
                'Contact_Number',
                'Activity',
                ]
        htmltbl = build_html_table(outputlist, dbcolumnlist, theadlist, "policy_benefit_business_asset_temp_table")
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-6">
                            <h4 class="card-title">Policy_benefit_business_asset_temp</h4>
                        </div>
                        <div class="col-md-6 text-right">
                            <button id="create_new_policy_benefit_business_asset_temp" class="btn btn-primary ml-auto">Create New Policy_benefit_business_asset_temp</button>
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
    def get_javascript_policy_benefit_business_asset_temp_onload(self, *args, **kwargs):
        javascript = """
        $("#create_new_policy_benefit_business_asset_temp").click(function(){
            $('#dialogdiv').load('/policy /get_modal_policy_benefit_business_asset_temp?', function(data){
                return false;
            });
        });
        $(".policy_benefit_business_asset_temp_edit").click(function(){
            var kwargs = 'policy_benefit_business_asset_temp_id='+$(this).attr('policy_benefit_business_asset_temp_id');
            $('#dialogdiv').load('/policy /get_modal_policy_benefit_business_asset_temp?', kwargs, function(data){
                return false;
            });
        });
        """
        return javascript

    @expose()
    def get_modal_policy_benefit_business_asset_temp(self, *args, **kwargs):
        policy_benefit_business_asset_temp_id = kwargs.get('policy_benefit_business_asset_temp_id', None)
        policy_benefit_business_asset_temp = None
        hidden_input = ''
        if policy_benefit_business_asset_temp_id:
            policy_benefit_business_asset_temp = PolicyBenefitBusinessAssetTemp.by_id(policy_benefit_business_asset_temp)
            hidden_input = get_hidden_input(**{'id': 'policy_benefit_business_asset_temp_id', 'value': policy_benefit_business_asset_temp_id})
        company_registration_number = policy_benefit_business_asset_temp.company_registration_number if policy_benefit_business_asset_temp else ''
        turnover = policy_benefit_business_asset_temp.turnover if policy_benefit_business_asset_temp else ''
        email = policy_benefit_business_asset_temp.email if policy_benefit_business_asset_temp else ''
        contact_name = policy_benefit_business_asset_temp.contact_name if policy_benefit_business_asset_temp else ''
        contact_number = policy_benefit_business_asset_temp.contact_number if policy_benefit_business_asset_temp else ''
        activity = policy_benefit_business_asset_temp.activity if policy_benefit_business_asset_temp else ''
        html = f"""
        <div class="modal fade" id="dialog_policy_benefit_business_asset_temp" tabindex="-1" role="dialog" aria-labelledby="mypolicy_benefit_business_asset_tempLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-6">
                            <h4 class="card-title">New Policy_benefit_business_asset_temp</h4>
                        </div>
                    </div>
                    <div class="modal-body">
                        <form id='form_new_policy_benefit_business_asset_temp'>
                        {hidden_input}
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="company_registration_number">Company_Registration_Number</label>
						<div class="col-md-9">
							<input id="company_registration_number" value="{company_registration_number}" type="text" name="company_registration_number" class="form-control" required='true'>
						</div>
					</div>
				</div>
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="turnover">Turnover</label>
						<div class="col-md-9">
							<input id="turnover" value="{turnover}" type="text" name="turnover" class="form-control" required='true'>
						</div>
					</div>
				</div>
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="email">Email</label>
						<div class="col-md-9">
							<input id="email" value="{email}" type="text" name="email" class="form-control" required='true'>
						</div>
					</div>
				</div>
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="contact_name">Contact_Name</label>
						<div class="col-md-9">
							<input id="contact_name" value="{contact_name}" type="text" name="contact_name" class="form-control" required='true'>
						</div>
					</div>
				</div>
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="contact_number">Contact_Number</label>
						<div class="col-md-9">
							<input id="contact_number" value="{contact_number}" type="text" name="contact_number" class="form-control" required='true'>
						</div>
					</div>
				</div>
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="activity">Activity</label>
						<div class="col-md-9">
							<input id="activity" value="{activity}" type="text" name="activity" class="form-control" required='true'>
						</div>
					</div>
				</div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button id='save_policy_benefit_business_asset_temp' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary policy_benefit_business_asset_temp_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
        var form_id = '#form_policy_benefit_business_asset_temp'
        setFormValidation(form_id);
        $('#save_policy_benefit_business_asset_temp').click(function(){
             var valid = FormIsValid(form_id);
             if(valid){
                var formserial = $(form_id).serialize();
                $.post('/policy /save_policy_benefit_business_asset_temp?', formserial, function(data){
                    $.redirect('/policy /policy_benefit_business_asset_temps');
                    return false;
                });
             }
        });
        $('.policy_benefit_business_asset_temp_back').click(function(){
            $('#dialog_policy_benefit_business_asset_temp').modal('hide');
        });
        $('#dialog_policy_benefit_business_asset_temp').modal();
        </script>
     	"""
        return html + javascript

    @expose()
    def save_policy_benefit_business_asset_temp(self, *args, **kwargs):
        usernow = request.identity.get('user', None)
        policy_benefit_business_asset_temp_id = kwargs.get('policy_benefit_business_asset_temp_id', None)
        if not policy_benefit_business_asset_temp_id:
            this = PolicyBenefitBusinessAssetTemp()
            this.policy_benefit_id = kwargs.get('policy_benefit_id', None)
            this.product_benefit_id = kwargs.get('product_benefit_id', None)
            this.company_registration_number = kwargs.get('company_registration_number', None)
            this.turnover = kwargs.get('turnover', None)
            this.email = kwargs.get('email', None)
            this.contact_name = kwargs.get('contact_name', None)
            this.contact_number = kwargs.get('contact_number', None)
            this.activity = kwargs.get('activity', None)
            this.added_by = usernow.id
            DBSession.add(this)
            DBSession.flush()
        else:
            this = PolicyBenefitBusinessAssetTemp.by_id(policy_benefit_business_asset_temp_id)
            if not this: return 'false'
            this.policy_benefit_id = kwargs.get('policy_benefit_id', None)
            this.product_benefit_id = kwargs.get('product_benefit_id', None)
            this.company_registration_number = kwargs.get('company_registration_number', None)
            this.turnover = kwargs.get('turnover', None)
            this.email = kwargs.get('email', None)
            this.contact_name = kwargs.get('contact_name', None)
            this.contact_number = kwargs.get('contact_number', None)
            this.activity = kwargs.get('activity', None)
            DBSession.flush()
        return str(this.id)
