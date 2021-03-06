#class_name = LoaderQuestion
#table_name = tbl_loader_question
#prefix =PRE
#postfix =POST
#columns_to_create = [id, text, loader_question_premium_effect_type_id] #id - primary_key autoincrement=True
#cont_name = setup
#html_template_name = generic
#dbsession = DBSession
#controller_name = SetupController
#view_cols_list = [text, loader_question_premium_effect_type_id]
#search_cols_list = [text, loader_question_premium_effect_type_id]
#pdf_cols_list = [text, loader_question_premium_effect_type_id]
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
#class_name = LoaderQuestion
#table_name =tbl_loader_question
#prefix =PRE
#postfix =POST
#columns_to_create = [id, text, loader_question_premium_effect_type_id] #id - primary_key autoincrement=True
#cont_name =setup
#html_template_name =generic
#dbsession =DBSession
#controller_name =SetupController
#view_cols_list = [text, loader_question_premium_effect_type_id]
#search_cols_list = [text, loader_question_premium_effect_type_id]
#pdf_cols_list = [text, loader_question_premium_effect_type_id]
#link_to_id_or_None =
#link_class_name_None =

############################
# Model
############################

class LoaderQuestion(DeclarativeBase):
    __tablename__='tbl_loader_question'
    id = Column(Integer, autoincrement=True, primary_key=True)
    text = Column(Unicode(255))
    loader_question_premium_effect_type_id = Column(Unicode(255))

    active = Column(Boolean, default=True)
    added_by = Column(Integer, nullable=False)
    added = Column(DateTime, default=datetime.now)

############################
# Controller
############################


class SetupController(BaseController):
    """Docstring for setup."""

    def __init__(self, *args, **kwargs):
        pass

    @require(predicates.not_anonymous())
    @expose('rocket_app.templates.generic')
    def tbl_loader_questions(self, *args, **kwargs):
        html = self.get_active_tbl_loader_question_html(*args, **kwargs)
        javascript = self.get_javascript_tbl_loader_question_onload()
        title = "Tbl_loader_question"
        return dict(title=title, html=html, javascript=javascript)

    @expose()
    def get_active_tbl_loader_question_html(self, *args, **kwargs):
        usernow = request.identity['user']
        dbase_query = self.get_active_tbl_loader_question_list(*args, **kwargs)
        outputlist = []
        for item in dbase_query:
            outputlist.append({
                'text' : "<div class='edit tbl_loader_question_edit' tbl_loader_question_id='{1}'>{0}</div>".format(item.text, item.id),
                'loader_question_premium_effect_type_id' : item.loader_question_premium_effect_type_id,
                             })
        dbcolumnlist=[
                'text',
                'loader_question_premium_effect_type_id',
                    ]
        theadlist=[
                'Text',
                'Loader_Question_Premium_Effect_Type_Id',
                ]
        tbl_loader_questiontable = build_html_table(outputlist, dbcolumnlist, theadlist, "tbl_loader_question_table")
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-6">
                            <h4 class="card-title">Tbl_loader_question</h4>
                        </div>
                        <div class="col-md-6 text-right">
                            <button id="create_new_tbl_loader_question" class="btn btn-primary ml-auto">Create a new Tbl_loader_question</button>
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
                        {tbl_loader_questiontable}
                    </div>
                </div>
                </div>
            </div>
            <div id='dialogdiv'></div>
        """
        return html

    @expose()
    def get_javascript_tbl_loader_question_onload(self, *args, **kwargs):
        javascript = """
        $("#create_new_tbl_loader_question").click(function(){
            $('#dialogdiv').load('/setup/get_modal_new_tbl_loader_question?', function(data){
                return false;
            });
        });
        $(".tbl_loader_question_edit").click(function(){
            var kwargs = 'tbl_loader_question_id='+$(this).attr('tbl_loader_question_id');
            $('#dialogdiv').load('/setup/get_modal_edit_tbl_loader_question?'+kwargs, function(data){
                return false;
            });
        });
        """
        return javascript

    @expose()
    def get_modal_new_tbl_loader_question(self, *args, **kwargs):
        html = """
        <div class="modal fade" id="dialog_new_tbl_loader_question" tabindex="-1" role="dialog" aria-labelledby="mytbl_loader_questionLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-6">
                            <h4 class="card-title">New Tbl_loader_question</h4>
                        </div>
                    </div>
                    <div class="modal-body">
                        <form id='form_new_tbl_loader_question'>
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="text">Text</label>
						<div class="col-md-9">
							<input id="text" type="text" name="text" class="form-control" required='true'>
						</div>
					</div>
				</div>
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="loader_question_premium_effect_type_id">Loader_Question_Premium_Effect_Type_Id</label>
						<div class="col-md-9">
							<input id="loader_question_premium_effect_type_id" type="text" name="loader_question_premium_effect_type_id" class="form-control" required='true'>
						</div>
					</div>
				</div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button id='save_new_tbl_loader_question' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary tbl_loader_question_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
        setFormValidation('#form_new_tbl_loader_question');
        $('#save_new_tbl_loader_question').click(function(){
             var valid = FormIsValid("#form_new_tbl_loader_question");
             if(valid){
                var formserial = getFormData('#form_new_tbl_loader_question');
                var data = {data : JSON.stringify(formserial)};

                $.post('/setup/save_new_tbl_loader_question?', data, function(data){
                    var result = JSON.parse(data);
                    if(result.success === true){
                        $.redirect('/setup/tbl_loader_questions');
                    };
                    return false;
                });
             }
        });
        $('.tbl_loader_question_back').click(function(){
            $('#dialog_new_tbl_loader_question').modal('hide');
        });
        $('#dialog_new_tbl_loader_question').modal();
        </script>
     	"""
        return html + javascript

    @expose()
    def get_modal_edit_tbl_loader_question(self, *args, **kwargs):
        tbl_loader_question_id = kwargs.get('tbl_loader_question_id', None)
        if not tbl_loader_question_id: return ''
        this = self.get_tbl_loader_question_by_id(*args, **kwargs)
        if not this: return ''
        checked = 'checked' if this.active else ''
        html = f"""
        <div class="modal fade" id="dialog_edit_tbl_loader_question" tabindex="-1" role="dialog" aria-labelledby="mytbl_loader_questionLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-6">
                            <h4 class="card-title">New Tbl_loader_question</h4>
                        </div>
                    </div>
                    <div class="modal-body">
                        <form id='form_edit_tbl_loader_question'>
                            <div style='display: none' class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="tbl_loader_question_id">Id</label>
						<div class="col-md-9">
							<input id="id" type="text" name="tbl_loader_question_id" value="{this.id}" class="form-control" required='true'>
						</div>
					</div>
				</div>
                            <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="text">Text</label>
						<div class="col-md-9">
							<input id="text" type="text" name="text" value="{this.text}" class="form-control" required='true'>
						</div>
					</div>
				</div>
                            <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="loader_question_premium_effect_type_id">Loader_Question_Premium_Effect_Type_Id</label>
						<div class="col-md-9">
							<input id="loader_question_premium_effect_type_id" type="text" name="loader_question_premium_effect_type_id" value="{this.loader_question_premium_effect_type_id}" class="form-control" required='true'>
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
                        <button id='save_edit_tbl_loader_question' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary tbl_loader_question_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
        setFormValidation('#form_edit_tbl_loader_question');
        $('#save_edit_tbl_loader_question').click(function(){
             var valid = FormIsValid("#form_edit_tbl_loader_question");
             if(valid){
                var formserial = getFormData('#form_edit_tbl_loader_question');
                var data = {data : JSON.stringify(formserial)};

                $.post('/setup/save_edit_tbl_loader_question?', data, function(data){
                    var result = JSON.parse(data);
                    if(result.success === true){
                        $.redirect('/setup/tbl_loader_questions');
                    };
                    return false;
                });
             }
        });
        $('.tbl_loader_question_back').click(function(){
            $('#dialog_edit_tbl_loader_question').modal('hide');
        });
        $('#dialog_edit_tbl_loader_question').modal();
        </script>
     	"""
        return html + javascript

    @expose()
    def save_new_tbl_loader_question(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        if not data: return json.dumps({'success' : False, 'data' : 'No data provided'})
        usernow = request.identity['user']
        this = LoaderQuestion()
        this.text = data.get('text', None)
        this.loader_question_premium_effect_type_id = data.get('loader_question_premium_effect_type_id', None)
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()
        return json.dumps({'success' : True, 'data' : this.id})

    @expose()
    def save_edit_tbl_loader_question(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        if not data: return json.dumps({'success' : False, 'data' : 'No data provided'})
        usernow = request.identity['user']
        this = self.get_tbl_loader_question_by_id(**data)
        if not this: return json.dumps({'success' : False, 'data' : 'No tbl_loader_question found for id provided'})
        this.text = data.get('text', None)
        this.loader_question_premium_effect_type_id = data.get('loader_question_premium_effect_type_id', None)
        if not data.get('active', None): this.active = False
        DBSession.flush()
        return json.dumps({'success' : True, 'data' : this.id})

    @expose()
    def get_tbl_loader_question_by_id(self, *args, **kwargs):
        return DBSession.query(LoaderQuestion). \
            filter(LoaderQuestion.id==kwargs.get('tbl_loader_question_id', None)). \
            first()

    @expose()
    def get_active_tbl_loader_question_list(self, *args, **kwargs):
        searchphrase = kwargs.get('searchphrase', None)

        text = kwargs.get('text', None)
        tbl_loader_question_loader_question_premium_effect_type_id = kwargs.get('tbl_loader_question_loader_question_premium_effect_type_id', None)

        if text:
            searchphrase = "%"+kwargs['text']+"%"
            dbase_query = DBSession.query(LoaderQuestion). \
			filter(LoaderQuestion.text.like(searchphrase)). \
                        filter(LoaderQuestion.active==1). \
			order_by(asc(LoaderQuestion.text)).limit(LIMIT)
        if tbl_loader_question_loader_question_premium_effect_type_id:
            dbase_query = DBSession.query(LoaderQuestion). \
		    filter(LoaderQuestion.tbl_loader_question_loader_question_premium_effect_type_id==tbl_loader_question_loader_question_premium_effect_type_id). \
                        filter(LoaderQuestion.active==1). \
		    order_by(asc(LoaderQuestion.tbl_loader_question_id)).limit(LIMIT)
        else:
            dbase_query = DBSession.query(LoaderQuestion). \
                filter(LoaderQuestion.active==1). \
                order_by(asc(LoaderQuestion.id)). \
                limit(LIMIT)
        return dbase_query
