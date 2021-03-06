#class_name = EntityClient
#table_name = tbl_entity_client
#prefix =PRE
#postfix =POST
#columns_to_create = [id, entity_organisation_id, billing_frequency_id, last_payment_date, last_invoice_date] #id - primary_key autoincrement=True
#cont_name = entity
#html_template_name = generic
#dbsession = DBSession
#controller_name = EntityController
#view_cols_list = [entity_organisation_id, billing_frequency_id, last_payment_date, last_invoice_date]
#search_cols_list = [entity_organisation_id, billing_frequency_id, last_payment_date, last_invoice_date]
#pdf_cols_list = [entity_organisation_id, billing_frequency_id, last_payment_date, last_invoice_date]
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
#class_name = EntityClient
#table_name =tbl_entity_client
#prefix =PRE
#postfix =POST
#columns_to_create = [id, entity_organisation_id, billing_frequency_id, last_payment_date, last_invoice_date] #id - primary_key autoincrement=True
#cont_name =entity
#html_template_name =generic
#dbsession =DBSession
#controller_name =EntityController
#view_cols_list = [entity_organisation_id, billing_frequency_id, last_payment_date, last_invoice_date]
#search_cols_list = [entity_organisation_id, billing_frequency_id, last_payment_date, last_invoice_date]
#pdf_cols_list = [entity_organisation_id, billing_frequency_id, last_payment_date, last_invoice_date]
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
    def tbl_entity_clients(self, *args, **kwargs):
        html = self.get_active_tbl_entity_client_html(*args, **kwargs)
        javascript = self.get_javascript_tbl_entity_client_onload()
        title = "Tbl_entity_client"
        return dict(title=title, html=html, javascript=javascript)

    @expose()
    def get_active_tbl_entity_client_html(self, *args, **kwargs):
        usernow = request.identity['user']
        dbase_query = self.get_active_tbl_entity_client_list(*args, **kwargs)
        outputlist = []
        for item in dbase_query:
            outputlist.append({
                'entity_organisation_id' : "<div class='edit tbl_entity_client_edit' tbl_entity_client_id='{1}'>{0}</div>".format(item.entity_organisation_id, item.id),
                'billing_frequency_id' : item.billing_frequency_id,
                'last_payment_date' : item.last_payment_date,
                'last_invoice_date' : item.last_invoice_date,
                             })
        dbcolumnlist=[
                'entity_organisation_id',
                'billing_frequency_id',
                'last_payment_date',
                'last_invoice_date',
                    ]
        theadlist=[
                'Entity_Organisation_Id',
                ' Billing_Frequency_Id',
                ' Last_Payment_Date',
                ' Last_Invoice_Date',
                ]
        tbl_entity_clienttable = build_html_table(outputlist, dbcolumnlist, theadlist, "tbl_entity_client_table")
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-6">
                            <h4 class="card-title">Tbl_entity_client</h4>
                        </div>
                        <div class="col-md-6 text-right">
                            <button id="create_new_tbl_entity_client" class="btn btn-primary ml-auto">Create a new Tbl_entity_client</button>
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
                        {tbl_entity_clienttable}
                    </div>
                </div>
                </div>
            </div>
            <div id='dialogdiv'></div>
        """
        return html

    @expose()
    def get_javascript_tbl_entity_client_onload(self, *args, **kwargs):
        javascript = """
        $("#create_new_tbl_entity_client").click(function(){
            $('#dialogdiv').load('/entity/get_modal_new_tbl_entity_client?', function(data){
                return false;
            });
        });
        $(".tbl_entity_client_edit").click(function(){
            var kwargs = 'tbl_entity_client_id='+$(this).attr('tbl_entity_client_id');
            $('#dialogdiv').load('/entity/get_modal_edit_tbl_entity_client?'+kwargs, function(data){
                return false;
            });
        });
        """
        return javascript

    @expose()
    def get_modal_new_tbl_entity_client(self, *args, **kwargs):
        html = """
        <div class="modal fade" id="dialog_new_tbl_entity_client" tabindex="-1" role="dialog" aria-labelledby="mytbl_entity_clientLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-6">
                            <h4 class="card-title">New Tbl_entity_client</h4>
                        </div>
                    </div>
                    <div class="modal-body">
                        <form id='form_new_tbl_entity_client'>
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="entity_organisation_id">Entity_Organisation_Id</label>
						<div class="col-md-9">
							<input id="entity_organisation_id" type="text" name="entity_organisation_id" class="form-control" required='true'>
						</div>
					</div>
				</div>
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="billing_frequency_id"> Billing_Frequency_Id</label>
						<div class="col-md-9">
							<input id="billing_frequency_id" type="text" name="billing_frequency_id" class="form-control" required='true'>
						</div>
					</div>
				</div>
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="last_payment_date"> Last_Payment_Date</label>
						<div class="col-md-9">
							<input id="last_payment_date" type="text" name="last_payment_date" class="form-control" required='true'>
						</div>
					</div>
				</div>
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="last_invoice_date"> Last_Invoice_Date</label>
						<div class="col-md-9">
							<input id="last_invoice_date" type="text" name="last_invoice_date" class="form-control" required='true'>
						</div>
					</div>
				</div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button id='save_new_tbl_entity_client' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary tbl_entity_client_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
        setFormValidation('#form_new_tbl_entity_client');
        $("#last_payment_date").datetimepicker({ format: 'DD/MM/YYYY' });
        $("#last_invoice_date").datetimepicker({ format: 'DD/MM/YYYY' });
        $('#save_new_tbl_entity_client').click(function(){
             var valid = FormIsValid("#form_new_tbl_entity_client");
             if(valid){
                var formserial = getFormData('#form_new_tbl_entity_client');
                var data = {data : JSON.stringify(formserial)};

                $.post('/entity/save_new_tbl_entity_client?', data, function(data){
                    var result = JSON.parse(data);
                    if(result.success === true){
                        $.redirect('/entity/tbl_entity_clients');
                    };
                    return false;
                });
             }
        });
        $('.tbl_entity_client_back').click(function(){
            $('#dialog_new_tbl_entity_client').modal('hide');
        });
        $('#dialog_new_tbl_entity_client').modal();
        </script>
     	"""
        return html + javascript

    @expose()
    def get_modal_edit_tbl_entity_client(self, *args, **kwargs):
        tbl_entity_client_id = kwargs.get('tbl_entity_client_id', None)
        if not tbl_entity_client_id: return ''
        this = self.get_tbl_entity_client_by_id(*args, **kwargs)
        if not this: return ''
        checked = 'checked' if this.active else ''
        html = f"""
        <div class="modal fade" id="dialog_edit_tbl_entity_client" tabindex="-1" role="dialog" aria-labelledby="mytbl_entity_clientLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-6">
                            <h4 class="card-title">New Tbl_entity_client</h4>
                        </div>
                    </div>
                    <div class="modal-body">
                        <form id='form_edit_tbl_entity_client'>
                            <div style='display: none' class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="tbl_entity_client_id">Id</label>
						<div class="col-md-9">
							<input id="id" type="text" name="tbl_entity_client_id" value="{this.id}" class="form-control" required='true'>
						</div>
					</div>
				</div>
                            <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="entity_organisation_id"> Entity_Organisation_Id</label>
						<div class="col-md-9">
							<input id="entity_organisation_id" type="text" name="entity_organisation_id" value="{this.entity_organisation_id}" class="form-control" required='true'>
						</div>
					</div>
				</div>
                            <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="billing_frequency_id"> Billing_Frequency_Id</label>
						<div class="col-md-9">
							<input id="billing_frequency_id" type="text" name="billing_frequency_id" value="{this.billing_frequency_id}" class="form-control" required='true'>
						</div>
					</div>
				</div>
                            <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="last_payment_date"> Last_Payment_Date</label>
						<div class="col-md-9">
							<input id="last_payment_date" type="text" name="last_payment_date" value="{this.last_payment_date}" class="form-control" required='true'>
						</div>
					</div>
				</div>
                            <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="last_invoice_date"> Last_Invoice_Date</label>
						<div class="col-md-9">
							<input id="last_invoice_date" type="text" name="last_invoice_date" value="{this.last_invoice_date}" class="form-control" required='true'>
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
                        <button id='save_edit_tbl_entity_client' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary tbl_entity_client_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
        setFormValidation('#form_edit_tbl_entity_client');
        $("#last_payment_date").datetimepicker({ format: 'DD/MM/YYYY' });
        $("#last_invoice_date").datetimepicker({ format: 'DD/MM/YYYY' });
        $('#save_edit_tbl_entity_client').click(function(){
             var valid = FormIsValid("#form_edit_tbl_entity_client");
             if(valid){
                var formserial = getFormData('#form_edit_tbl_entity_client');
                var data = {data : JSON.stringify(formserial)};

                $.post('/entity/save_edit_tbl_entity_client?', data, function(data){
                    var result = JSON.parse(data);
                    if(result.success === true){
                        $.redirect('/entity/tbl_entity_clients');
                    };
                    return false;
                });
             }
        });
        $('.tbl_entity_client_back').click(function(){
            $('#dialog_edit_tbl_entity_client').modal('hide');
        });
        $('#dialog_edit_tbl_entity_client').modal();
        </script>
     	"""
        return html + javascript

    @expose()
    def save_new_tbl_entity_client(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        if not data: return json.dumps({'success' : False, 'data' : 'No data provided'})
        usernow = request.identity['user']
        this = EntityClient()
        this.entity_organisation_id = data.get('entity_organisation_id', None)
        this.billing_frequency_id = data.get('billing_frequency_id', None)
        this.last_payment_date = data.get('last_payment_date', None)
        this.last_invoice_date = data.get('last_invoice_date', None)
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()
        return json.dumps({'success' : True, 'data' : this.id})

    @expose()
    def save_edit_tbl_entity_client(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        if not data: return json.dumps({'success' : False, 'data' : 'No data provided'})
        usernow = request.identity['user']
        this = self.get_tbl_entity_client_by_id(**data)
        if not this: return json.dumps({'success' : False, 'data' : 'No tbl_entity_client found for id provided'})
        this.entity_organisation_id = data.get('entity_organisation_id', None)
        this.billing_frequency_id = data.get('billing_frequency_id', None)
        this.last_payment_date = data.get('last_payment_date', None)
        this.last_invoice_date = data.get('last_invoice_date', None)
        if not data.get('active', None): this.active = False
        DBSession.flush()
        return json.dumps({'success' : True, 'data' : this.id})

    @expose()
    def get_tbl_entity_client_by_id(self, *args, **kwargs):
        return DBSession.query(EntityClient). \
            filter(EntityClient.id==kwargs.get('tbl_entity_client_id', None)). \
            first()

    @expose()
    def get_active_tbl_entity_client_list(self, *args, **kwargs):
        searchphrase = kwargs.get('searchphrase', None)

        tbl_entity_client_entity_organisation_id = kwargs.get('tbl_entity_client_entity_organisation_id', None)
        tbl_entity_client_billing_frequency_id = kwargs.get('tbl_entity_client_billing_frequency_id', None)
        last_payment_date_start = kwargs.get('last_payment_date_start', None)
        last_payment_date_end = kwargs.get('last_payment_date_end', None)
        last_invoice_date_start = kwargs.get('last_invoice_date_start', None)
        last_invoice_date_end = kwargs.get('last_invoice_date_end', None)

        if tbl_entity_client_entity_organisation_id:
            dbase_query = DBSession.query(EntityClient). \
		    filter(EntityClient.tbl_entity_client_entity_organisation_id==tbl_entity_client_entity_organisation_id). \
                        filter(EntityClient.active==1). \
		    order_by(asc(EntityClient.tbl_entity_client_id)).limit(LIMIT)
        if tbl_entity_client_billing_frequency_id:
            dbase_query = DBSession.query(EntityClient). \
		    filter(EntityClient.tbl_entity_client_billing_frequency_id==tbl_entity_client_billing_frequency_id). \
                        filter(EntityClient.active==1). \
		    order_by(asc(EntityClient.tbl_entity_client_id)).limit(LIMIT)
        if last_payment_date_start:
            if not last_payment_date_end: last_payment_date_end = datetime.date(datetime.now())
            dbase_query = DBSession.query(EntityClient). \
			filter(EntityClient.last_payment_date>=last_payment_date_start). \
			filter(EntityClient.last_payment_date<=last_payment_date_end). \
                        filter(EntityClient.active==1). \
			order_by(asc(EntityClient.id)).limit(LIMIT)
        if last_invoice_date_start:
            if not last_invoice_date_end: last_invoice_date_end = datetime.date(datetime.now())
            dbase_query = DBSession.query(EntityClient). \
			filter(EntityClient.last_invoice_date>=last_invoice_date_start). \
			filter(EntityClient.last_invoice_date<=last_invoice_date_end). \
                        filter(EntityClient.active==1). \
			order_by(asc(EntityClient.id)).limit(LIMIT)
        else:
            dbase_query = DBSession.query(EntityClient). \
                filter(EntityClient.active==1). \
                order_by(asc(EntityClient.id)). \
                limit(LIMIT)
        return dbase_query
