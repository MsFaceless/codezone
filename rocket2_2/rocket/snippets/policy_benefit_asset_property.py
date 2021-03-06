#class_name = PolicyBenefitPropertyAssetTemp
#table_name = policy_benefit_property_asset_temp
#prefix =PRE
#postfix =POST
#columns_to_create = [id, policy_benefit_id, product_benefit_id, number_of_premises, is_owned, is_shared, number_of_shared] #id - primary_key autoincrement=True
#cont_name =policy
#html_template_name = generic
#dbsession = DBSession
#controller_name = PolicyController
#view_cols_list = [number_of_premises, is_owned, is_shared, number_of_shared]
#search_cols_list = [number_of_premises, is_owned, is_shared, number_of_shared]
#pdf_cols_list = [number_of_premises, is_owned, is_shared, number_of_shared]
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
#class_name = PolicyBenefitPropertyAssetTemp
#table_name =policy_benefit_property_asset_temp
#prefix =PRE
#postfix =POST
#columns_to_create = [id, policy_benefit_id, product_benefit_id, number_of_premises, is_owned, is_shared, number_of_shared] #id - primary_key autoincrement=True
#cont_name =policy
#html_template_name =generic
#dbsession =DBSession
#controller_name =PolicyController
#view_cols_list = [number_of_premises, is_owned, is_shared, number_of_shared]
#search_cols_list = [number_of_premises, is_owned, is_shared, number_of_shared]
#pdf_cols_list = [number_of_premises, is_owned, is_shared, number_of_shared]
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
    def policy_benefit_property_asset_temps(self, *args, **kwargs):
        html = self.get_active_policy_benefit_property_asset_temp_html(*args, **kwargs)
        javascript = self.get_javascript_policy_benefit_property_asset_temp_onload()
        title = "Policy_benefit_property_asset_temp"
        return dict(title=title, html=html, javascript=javascript)

    @expose()
    def get_active_policy_benefit_property_asset_temp_html(self, *args, **kwargs):
        dbase_query = PolicyBenefitPropertyAssetTemp.get_all('id')
        outputlist = []
        for item in dbase_query:
            outputlist.append({
                'number_of_premises' : "<div class='edit policy_benefit_property_asset_temp_edit' policy_benefit_property_asset_temp_id='{1}'>{0}</div>".format(item.number_of_premises, item.id),
                'is_owned' : item.is_owned,
                'is_shared' : item.is_shared,
                'number_of_shared' : item.number_of_shared,
                             })
        dbcolumnlist=[
                'number_of_premises',
                'is_owned',
                'is_shared',
                'number_of_shared',
                    ]
        theadlist=[
                'Number_Of_Premises',
                'Is_Owned',
                'Is_Shared',
                'Number_Of_Shared',
                ]
        htmltbl = build_html_table(outputlist, dbcolumnlist, theadlist, "policy_benefit_property_asset_temp_table")
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-6">
                            <h4 class="card-title">Policy_benefit_property_asset_temp</h4>
                        </div>
                        <div class="col-md-6 text-right">
                            <button id="create_new_policy_benefit_property_asset_temp" class="btn btn-primary ml-auto">Create New Policy_benefit_property_asset_temp</button>
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
    def get_javascript_policy_benefit_property_asset_temp_onload(self, *args, **kwargs):
        javascript = """
        $("#create_new_policy_benefit_property_asset_temp").click(function(){
            $('#dialogdiv').load('/policy /get_modal_policy_benefit_property_asset_temp?', function(data){
                return false;
            });
        });
        $(".policy_benefit_property_asset_temp_edit").click(function(){
            var kwargs = 'policy_benefit_property_asset_temp_id='+$(this).attr('policy_benefit_property_asset_temp_id');
            $('#dialogdiv').load('/policy /get_modal_policy_benefit_property_asset_temp?', kwargs, function(data){
                return false;
            });
        });
        """
        return javascript

    @expose()
    def get_modal_policy_benefit_property_asset_temp(self, *args, **kwargs):
        policy_benefit_property_asset_temp_id = kwargs.get('policy_benefit_property_asset_temp_id', None)
        policy_benefit_property_asset_temp = None
        hidden_input = ''
        if policy_benefit_property_asset_temp_id:
            policy_benefit_property_asset_temp = PolicyBenefitPropertyAssetTemp.by_id(policy_benefit_property_asset_temp)
            hidden_input = get_hidden_input(**{'id': 'policy_benefit_property_asset_temp_id', 'value': policy_benefit_property_asset_temp_id})
        number_of_premises = policy_benefit_property_asset_temp.number_of_premises if policy_benefit_property_asset_temp else ''
        is_owned = policy_benefit_property_asset_temp.is_owned if policy_benefit_property_asset_temp else ''
        is_shared = policy_benefit_property_asset_temp.is_shared if policy_benefit_property_asset_temp else ''
        number_of_shared = policy_benefit_property_asset_temp.number_of_shared if policy_benefit_property_asset_temp else ''
        html = f"""
        <div class="modal fade" id="dialog_policy_benefit_property_asset_temp" tabindex="-1" role="dialog" aria-labelledby="mypolicy_benefit_property_asset_tempLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-6">
                            <h4 class="card-title">New Policy_benefit_property_asset_temp</h4>
                        </div>
                    </div>
                    <div class="modal-body">
                        <form id='form_new_policy_benefit_property_asset_temp'>
                        {hidden_input}
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="number_of_premises">Number_Of_Premises</label>
						<div class="col-md-9">
							<input id="number_of_premises" value="{number_of_premises}" type="text" name="number_of_premises" class="form-control" required='true'>
						</div>
					</div>
				</div>
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="is_owned">Is_Owned</label>
						<div class="col-md-9">
							<input id="is_owned" value="{is_owned}" type="text" name="is_owned" class="form-control" required='true'>
						</div>
					</div>
				</div>
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="is_shared">Is_Shared</label>
						<div class="col-md-9">
							<input id="is_shared" value="{is_shared}" type="text" name="is_shared" class="form-control" required='true'>
						</div>
					</div>
				</div>
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="number_of_shared">Number_Of_Shared</label>
						<div class="col-md-9">
							<input id="number_of_shared" value="{number_of_shared}" type="text" name="number_of_shared" class="form-control" required='true'>
						</div>
					</div>
				</div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button id='save_policy_benefit_property_asset_temp' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary policy_benefit_property_asset_temp_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
        var form_id = '#form_policy_benefit_property_asset_temp'
        setFormValidation(form_id);
        $('#save_policy_benefit_property_asset_temp').click(function(){
             var valid = FormIsValid(form_id);
             if(valid){
                var formserial = $(form_id).serialize();
                $.post('/policy /save_policy_benefit_property_asset_temp?', formserial, function(data){
                    $.redirect('/policy /policy_benefit_property_asset_temps');
                    return false;
                });
             }
        });
        $('.policy_benefit_property_asset_temp_back').click(function(){
            $('#dialog_policy_benefit_property_asset_temp').modal('hide');
        });
        $('#dialog_policy_benefit_property_asset_temp').modal();
        </script>
     	"""
        return html + javascript

    @expose()
    def save_policy_benefit_property_asset_temp(self, *args, **kwargs):
        usernow = request.identity.get('user', None)
        policy_benefit_property_asset_temp_id = kwargs.get('policy_benefit_property_asset_temp_id', None)
        if not policy_benefit_property_asset_temp_id:
            this = PolicyBenefitPropertyAssetTemp()
            this.policy_benefit_id = kwargs.get('policy_benefit_id', None)
            this.product_benefit_id = kwargs.get('product_benefit_id', None)
            this.number_of_premises = kwargs.get('number_of_premises', None)
            this.is_owned = kwargs.get('is_owned', None)
            this.is_shared = kwargs.get('is_shared', None)
            this.number_of_shared = kwargs.get('number_of_shared', None)
            this.added_by = usernow.id
            DBSession.add(this)
            DBSession.flush()
        else:
            this = PolicyBenefitPropertyAssetTemp.by_id(policy_benefit_property_asset_temp_id)
            if not this: return 'false'
            this.policy_benefit_id = kwargs.get('policy_benefit_id', None)
            this.product_benefit_id = kwargs.get('product_benefit_id', None)
            this.number_of_premises = kwargs.get('number_of_premises', None)
            this.is_owned = kwargs.get('is_owned', None)
            this.is_shared = kwargs.get('is_shared', None)
            this.number_of_shared = kwargs.get('number_of_shared', None)
            DBSession.flush()
        return str(this.id)
