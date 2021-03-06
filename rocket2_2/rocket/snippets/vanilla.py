#class_name = ProductMessage
#table_name = tbl_product_message
#prefix =PRE
#postfix =POST
#columns_to_create = [id, product_id, product_message_type_id, product_communication_type_id, name] #id - primary_key autoincrement=True
#cont_name = product
#html_template_name = generic
#dbsession = DBSession
#controller_name = ProductController
#view_cols_list = [product_id, product_message_type_id, product_communication_type_id, name]
#search_cols_list = [product_id, product_message_type_id, product_communication_type_id, name]
#pdf_cols_list = [product_id, product_message_type_id, product_communication_type_id, name]
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
#class_name = ProductMessage
#table_name =tbl_product_message
#prefix =PRE
#postfix =POST
#columns_to_create = [id, product_id, product_message_type_id, product_communication_type_id, name] #id - primary_key autoincrement=True
#cont_name =product
#html_template_name =generic
#dbsession =DBSession
#controller_name =ProductController
#view_cols_list = [product_id, product_message_type_id, product_communication_type_id, name]
#search_cols_list = [product_id, product_message_type_id, product_communication_type_id, name]
#pdf_cols_list = [product_id, product_message_type_id, product_communication_type_id, name]
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
    def tbl_product_messages(self, *args, **kwargs):
        html = self.get_active_tbl_product_message_html(*args, **kwargs)
        javascript = self.get_javascript_tbl_product_message_onload()
        title = "Tbl_product_message"
        return dict(title=title, html=html, javascript=javascript)

    @expose()
    def get_active_tbl_product_message_html(self, *args, **kwargs):
        usernow = request.identity['user']
        dbase_query = self.get_active_tbl_product_message_list(*args, **kwargs)
        outputlist = []
        for item in dbase_query:
            outputlist.append({
                'product_id' : "<div class='edit tbl_product_message_edit' tbl_product_message_id='{1}'>{0}</div>".format(item.product_id, item.id),
                'product_message_type_id' : item.product_message_type_id,
                'product_communication_type_id' : item.product_communication_type_id,
                'name' : item.name,
                             })
        dbcolumnlist=[
                'product_id',
                'product_message_type_id',
                'product_communication_type_id',
                'name',
                    ]
        theadlist=[
                'Product_Id',
                'Product_Message_Type_Id',
                'Product_Communication_Type_Id',
                'Name',
                ]
        tbl_product_messagetable = build_html_table(outputlist, dbcolumnlist, theadlist, "tbl_product_message_table")
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-6">
                            <h4 class="card-title">Tbl_product_message</h4>
                        </div>
                        <div class="col-md-6 text-right">
                            <button id="create_new_tbl_product_message" class="btn btn-primary ml-auto">Create a new Tbl_product_message</button>
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
                        {tbl_product_messagetable}
                    </div>
                </div>
                </div>
            </div>
            <div id='dialogdiv'></div>
        """
        return html

    @expose()
    def get_javascript_tbl_product_message_onload(self, *args, **kwargs):
        javascript = """
        $("#create_new_tbl_product_message").click(function(){
            $('#dialogdiv').load('/product/get_modal_new_tbl_product_message?', function(data){
                return false;
            });
        });
        $(".tbl_product_message_edit").click(function(){
            var kwargs = 'tbl_product_message_id='+$(this).attr('tbl_product_message_id');
            $('#dialogdiv').load('/product/get_modal_edit_tbl_product_message?'+kwargs, function(data){
                return false;
            });
        });
        """
        return javascript

    @expose()
    def get_modal_new_tbl_product_message(self, *args, **kwargs):
        html = """
        <div class="modal fade" id="dialog_new_tbl_product_message" tabindex="-1" role="dialog" aria-labelledby="mytbl_product_messageLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-6">
                            <h4 class="card-title">New Tbl_product_message</h4>
                        </div>
                    </div>
                    <div class="modal-body">
                        <form id='form_new_tbl_product_message'>
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="product_id">Product_Id</label>
						<div class="col-md-9">
							<input id="product_id" type="text" name="product_id" class="form-control" required='true'>
						</div>
					</div>
				</div>
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="product_message_type_id">Product_Message_Type_Id</label>
						<div class="col-md-9">
							<input id="product_message_type_id" type="text" name="product_message_type_id" class="form-control" required='true'>
						</div>
					</div>
				</div>
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="product_communication_type_id">Product_Communication_Type_Id</label>
						<div class="col-md-9">
							<input id="product_communication_type_id" type="text" name="product_communication_type_id" class="form-control" required='true'>
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
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button id='save_new_tbl_product_message' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary tbl_product_message_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
        setFormValidation('#form_new_tbl_product_message');
        $('#save_new_tbl_product_message').click(function(){
             var valid = FormIsValid("#form_new_tbl_product_message");
             if(valid){
                var formserial = getFormData('#form_new_tbl_product_message');
                var data = {data : JSON.stringify(formserial)};

                $.post('/product/save_new_tbl_product_message?', data, function(data){
                    var result = JSON.parse(data);
                    if(result.success === true){
                        $.redirect('/product/tbl_product_messages');
                    };
                    return false;
                });
             }
        });
        $('.tbl_product_message_back').click(function(){
            $('#dialog_new_tbl_product_message').modal('hide');
        });
        $('#dialog_new_tbl_product_message').modal();
        </script>
     	"""
        return html + javascript

    @expose()
    def get_modal_edit_tbl_product_message(self, *args, **kwargs):
        tbl_product_message_id = kwargs.get('tbl_product_message_id', None)
        if not tbl_product_message_id: return ''
        this = self.get_tbl_product_message_by_id(*args, **kwargs)
        if not this: return ''
        checked = 'checked' if this.active else ''
        html = f"""
        <div class="modal fade" id="dialog_edit_tbl_product_message" tabindex="-1" role="dialog" aria-labelledby="mytbl_product_messageLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-6">
                            <h4 class="card-title">New Tbl_product_message</h4>
                        </div>
                    </div>
                    <div class="modal-body">
                        <form id='form_edit_tbl_product_message'>
                            <div style='display: none' class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="tbl_product_message_id">Id</label>
						<div class="col-md-9">
							<input id="id" type="text" name="tbl_product_message_id" value="{this.id}" class="form-control" required='true'>
						</div>
					</div>
				</div>
                            <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="product_id">Product_Id</label>
						<div class="col-md-9">
							<input id="product_id" type="text" name="product_id" value="{this.product_id}" class="form-control" required='true'>
						</div>
					</div>
				</div>
                            <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="product_message_type_id">Product_Message_Type_Id</label>
						<div class="col-md-9">
							<input id="product_message_type_id" type="text" name="product_message_type_id" value="{this.product_message_type_id}" class="form-control" required='true'>
						</div>
					</div>
				</div>
                            <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="product_communication_type_id">Product_Communication_Type_Id</label>
						<div class="col-md-9">
							<input id="product_communication_type_id" type="text" name="product_communication_type_id" value="{this.product_communication_type_id}" class="form-control" required='true'>
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
                            <div class="form-group row">
                              <label class="col-4 col-form-label" for="active" required>Active</label>
                              <div class="col-8"><div class="form-check">
                                <input class="form-check-input" type="checkbox" name="active" id="active" {checked}/></div>
                              </div>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button id='save_edit_tbl_product_message' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary tbl_product_message_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
        setFormValidation('#form_edit_tbl_product_message');
        $('#save_edit_tbl_product_message').click(function(){
             var valid = FormIsValid("#form_edit_tbl_product_message");
             if(valid){
                var formserial = getFormData('#form_edit_tbl_product_message');
                var data = {data : JSON.stringify(formserial)};

                $.post('/product/save_edit_tbl_product_message?', data, function(data){
                    var result = JSON.parse(data);
                    if(result.success === true){
                        $.redirect('/product/tbl_product_messages');
                    };
                    return false;
                });
             }
        });
        $('.tbl_product_message_back').click(function(){
            $('#dialog_edit_tbl_product_message').modal('hide');
        });
        $('#dialog_edit_tbl_product_message').modal();
        </script>
     	"""
        return html + javascript

    @expose()
    def save_new_tbl_product_message(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        if not data: return json.dumps({'success' : False, 'data' : 'No data provided'})
        usernow = request.identity['user']
        this = ProductMessage()
        this.product_id = data.get('product_id', None)
        this.product_message_type_id = data.get('product_message_type_id', None)
        this.product_communication_type_id = data.get('product_communication_type_id', None)
        this.name = data.get('name', None)
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()
        return json.dumps({'success' : True, 'data' : this.id})

    @expose()
    def save_edit_tbl_product_message(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        if not data: return json.dumps({'success' : False, 'data' : 'No data provided'})
        usernow = request.identity['user']
        this = self.get_tbl_product_message_by_id(**data)
        if not this: return json.dumps({'success' : False, 'data' : 'No tbl_product_message found for id provided'})
        this.product_id = data.get('product_id', None)
        this.product_message_type_id = data.get('product_message_type_id', None)
        this.product_communication_type_id = data.get('product_communication_type_id', None)
        this.name = data.get('name', None)
        if not data.get('active', None): this.active = False
        DBSession.flush()
        return json.dumps({'success' : True, 'data' : this.id})

    @expose()
    def get_tbl_product_message_by_id(self, *args, **kwargs):
        return DBSession.query(ProductMessage). \
            filter(ProductMessage.id==kwargs.get('tbl_product_message_id', None)). \
            first()

    @expose()
    def get_active_tbl_product_message_list(self, *args, **kwargs):
        searchphrase = kwargs.get('searchphrase', None)

        tbl_product_message_product_id = kwargs.get('tbl_product_message_product_id', None)
        tbl_product_message_product_message_type_id = kwargs.get('tbl_product_message_product_message_type_id', None)
        tbl_product_message_product_communication_type_id = kwargs.get('tbl_product_message_product_communication_type_id', None)
        name = kwargs.get('name', None)

        if tbl_product_message_product_id:
            dbase_query = DBSession.query(ProductMessage). \
		    filter(ProductMessage.tbl_product_message_product_id==tbl_product_message_product_id). \
                        filter(ProductMessage.active==1). \
		    order_by(asc(ProductMessage.tbl_product_message_id)).limit(LIMIT)
        if tbl_product_message_product_message_type_id:
            dbase_query = DBSession.query(ProductMessage). \
		    filter(ProductMessage.tbl_product_message_product_message_type_id==tbl_product_message_product_message_type_id). \
                        filter(ProductMessage.active==1). \
		    order_by(asc(ProductMessage.tbl_product_message_id)).limit(LIMIT)
        if tbl_product_message_product_communication_type_id:
            dbase_query = DBSession.query(ProductMessage). \
		    filter(ProductMessage.tbl_product_message_product_communication_type_id==tbl_product_message_product_communication_type_id). \
                        filter(ProductMessage.active==1). \
		    order_by(asc(ProductMessage.tbl_product_message_id)).limit(LIMIT)
        if name:
            searchphrase = "%"+kwargs['name']+"%"
            dbase_query = DBSession.query(ProductMessage). \
			filter(ProductMessage.name.like(searchphrase)). \
                        filter(ProductMessage.active==1). \
			order_by(asc(ProductMessage.name)).limit(LIMIT)
        else:
            dbase_query = DBSession.query(ProductMessage). \
                filter(ProductMessage.active==1). \
                order_by(asc(ProductMessage.id)). \
                limit(LIMIT)
        return dbase_query
