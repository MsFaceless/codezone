#class_name = LoaderQuestionAnswer
#table_name = tbl_loader_question_answer
#prefix =PRE
#postfix =POST
#columns_to_create = [id, loader_question_id, answer_text, amount, percentage] #id - primary_key autoincrement=True
#cont_name = setup
#html_template_name = generic
#dbsession = DBSession
#controller_name = SetupController
#view_cols_list = [loader_question_id, answer_text, amount, percentage]
#search_cols_list = [loader_question_id, answer_text, amount, percentage]
#pdf_cols_list = [loader_question_id, answer_text, amount, percentage]
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
#class_name = LoaderQuestionAnswer
#table_name =tbl_loader_question_answer
#prefix =PRE
#postfix =POST
#columns_to_create = [id, loader_question_id, answer_text, amount, percentage] #id - primary_key autoincrement=True
#cont_name =setup
#html_template_name =generic
#dbsession =DBSession
#controller_name =SetupController
#view_cols_list = [loader_question_id, answer_text, amount, percentage]
#search_cols_list = [loader_question_id, answer_text, amount, percentage]
#pdf_cols_list = [loader_question_id, answer_text, amount, percentage]
#link_to_id_or_None =
#link_class_name_None =

############################
# Model
############################

class LoaderQuestionAnswer(DeclarativeBase):
    __tablename__='tbl_loader_question_answer'
    id = Column(Integer, autoincrement=True, primary_key=True)
    loader_question_id = Column(Unicode(255))
    answer_text = Column(Unicode(255))
    amount = Column(Unicode(255))
    percentage = Column(Unicode(255))

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
    def tbl_loader_question_answers(self, *args, **kwargs):
        html = self.get_active_tbl_loader_question_answer_html(*args, **kwargs)
        javascript = self.get_javascript_tbl_loader_question_answer_onload()
        title = "Tbl_loader_question_answer"
        return dict(title=title, html=html, javascript=javascript)

    @expose()
    def get_active_tbl_loader_question_answer_html(self, *args, **kwargs):
        usernow = request.identity['user']
        dbase_query = self.get_active_tbl_loader_question_answer_list(*args, **kwargs)
        outputlist = []
        for item in dbase_query:
            outputlist.append({
                'loader_question_id' : "<div class='edit tbl_loader_question_answer_edit' tbl_loader_question_answer_id='{1}'>{0}</div>".format(item.loader_question_id, item.id),
                'answer_text' : item.answer_text,
                'amount' : item.amount,
                'percentage' : item.percentage,
                             })
        dbcolumnlist=[
                'loader_question_id',
                'answer_text',
                'amount',
                'percentage',
                    ]
        theadlist=[
                'Loader_Question_Id',
                'Answer_Text',
                'Amount',
                'Percentage',
                ]
        tbl_loader_question_answertable = build_html_table(outputlist, dbcolumnlist, theadlist, "tbl_loader_question_answer_table")
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-6">
                            <h4 class="card-title">Tbl_loader_question_answer</h4>
                        </div>
                        <div class="col-md-6 text-right">
                            <button id="create_new_tbl_loader_question_answer" class="btn btn-primary ml-auto">Create a new Tbl_loader_question_answer</button>
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
                        {tbl_loader_question_answertable}
                    </div>
                </div>
                </div>
            </div>
        """
        return html

    @expose()
    def get_javascript_tbl_loader_question_answer_onload(self, *args, **kwargs):
        javascript = """
        $("#create_new_tbl_loader_question_answer").click(function(){
            $.redirect('/setup/new_tbl_loader_question_answer');
        });
        $(".tbl_loader_question_answer_edit").click(function(){
            var data = {tbl_loader_question_answer_id : $(this).attr('tbl_loader_question_answer_id')};
            $.redirect('/setup/edit_tbl_loader_question_answer', data);
        });
        """
        return javascript

    @expose('rocket_app.templates.generic')
    def new_tbl_loader_question_answer(self, *args, **kwargs):
        html = """
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-header d-flex">
                        <div class="col-md-6">
                            <h4 class="card-title">New Tbl_loader_question_answer</h4>
                        </div>
                        <div class="col-md-6 text-right">
                            <button class="btn btn-primary ml-auto action_back tbl_loader_question_answer_back">Back to Tbl_loader_question_answer List</button>
                        </div>
                    </div>
                    <div class="card-body">
                        <form id='form_new_tbl_loader_question_answer'>
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="loader_question_id">Loader_Question_Id</label>
						<div class="col-md-9">
							<input id="loader_question_id" type="text" name="loader_question_id" class="form-control" required='true'>
						</div>
					</div>
				</div>
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="answer_text">Answer_Text</label>
						<div class="col-md-9">
							<input id="answer_text" type="text" name="answer_text" class="form-control" required='true'>
						</div>
					</div>
				</div>
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="amount">Amount</label>
						<div class="col-md-9">
							<input id="amount" type="text" name="amount" class="form-control" required='true'>
						</div>
					</div>
				</div>
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="percentage">Percentage</label>
						<div class="col-md-9">
							<input id="percentage" type="text" name="percentage" class="form-control" required='true'>
						</div>
					</div>
				</div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-body">
                        <button id='save_new_tbl_loader_question_answer' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary tbl_loader_question_answer_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        setFormValidation('#form_new_tbl_loader_question_answer');
        $('#save_new_tbl_loader_question_answer').click(function(){
             var valid = FormIsValid("#form_new_tbl_loader_question_answer");
             if(valid){
                var formserial = getFormData('#form_new_tbl_loader_question_answer');
                var data = {data : JSON.stringify(formserial)};

                $.post('/setup/save_new_tbl_loader_question_answer?', data, function(data){
                    var result = JSON.parse(data);
                    if(result.success === true){
                        $.redirect('/setup/tbl_loader_question_answers');
                    };
                    return false;
                });
             }
        });
        $('.tbl_loader_question_answer_back').click(function(){
            $.redirect('/setup/tbl_loader_question_answers');
        });
     	"""
        title = "New Tbl_loader_question_answer"
        return dict(title=title, html=html, javascript=javascript)

    @expose('rocket_app.templates.generic')
    def edit_tbl_loader_question_answer(self, *args, **kwargs):
        tbl_loader_question_answer_id = kwargs.get('tbl_loader_question_answer_id', None)
        if not tbl_loader_question_answer_id: redirect('/setup/tbl_loader_question_answers')
        this = self.get_tbl_loader_question_answer_by_id(*args, **kwargs)
        if not this: redirect('/setup/tbl_loader_question_answers')
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-header d-flex">
                        <div class="col-md-6">
                            <h4 class="card-title">Edit Tbl_loader_question_answer</h4>
                        </div>
                        <div class="col-md-6 text-right">
                            <button class="btn btn-primary ml-auto action_back tbl_loader_question_answer_back">Back to Tbl_loader_question_answer List</button>
                        </div>
                    </div>
                    <div class="card-body">
                        <form id='form_edit_tbl_loader_question_answer'>
                                <div style='display: none' class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="tbl_loader_question_answer_id">Id</label>
						<div class="col-md-9">
							<input id="id" type="text" name="tbl_loader_question_answer_id" value="{this.id}" class="form-control" required='true'>
						</div>
					</div>
				</div>
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="loader_question_id">Loader_Question_Id</label>
						<div class="col-md-9">
							<input id="loader_question_id" type="text" name="loader_question_id" value="{this.loader_question_id}" class="form-control" required='true'>
						</div>
					</div>
				</div>
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="answer_text">Answer_Text</label>
						<div class="col-md-9">
							<input id="answer_text" type="text" name="answer_text" value="{this.answer_text}" class="form-control" required='true'>
						</div>
					</div>
				</div>
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="amount">Amount</label>
						<div class="col-md-9">
							<input id="amount" type="text" name="amount" value="{this.amount}" class="form-control" required='true'>
						</div>
					</div>
				</div>
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="percentage">Percentage</label>
						<div class="col-md-9">
							<input id="percentage" type="text" name="percentage" value="{this.percentage}" class="form-control" required='true'>
						</div>
					</div>
				</div>
                            <div class="col-md-12">
                                <div class="form-group row">
                                  <label class="col-3 col-form-label" for="active" required>Active</label>
                                  <div class="col-9"><div class="form-check">
                                      <label class="form-check-label">
                                        <input class="form-check-input" type="checkbox" name="active" id="active" {checked}/></div>
                                      </label>
                                  </div>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-body">
                        <button id='save_edit_tbl_loader_question_answer' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary tbl_loader_question_answer_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        setFormValidation('#form_edit_tbl_loader_question_answer');
        $('#save_edit_tbl_loader_question_answer').click(function(){
             var valid = FormIsValid("#form_edit_tbl_loader_question_answer");
             if(valid){
                var formserial = getFormData('#form_edit_tbl_loader_question_answer');
                var data = {data : JSON.stringify(formserial)};

                $.post('/setup/save_edit_tbl_loader_question_answer?', data, function(data){
                    var result = JSON.parse(data);
                    if(result.success === true){
                        $.redirect('/setup/tbl_loader_question_answers');
                    };
                    return false;
                });
             }
        });
        $('.tbl_loader_question_answer_back').click(function(){
            $.redirect('/setup/tbl_loader_question_answers');
        });
     	"""
        title = "Edit Tbl_loader_question_answer"
        return dict(title=title, html=html, javascript=javascript)

    @expose()
    def save_new_tbl_loader_question_answer(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        if not data: return json.dumps({'success' : False})
        usernow = request.identity['user']
        this = LoaderQuestionAnswer()
        this.loader_question_id = data.get('loader_question_id', None)
        this.answer_text = data.get('answer_text', None)
        this.amount = data.get('amount', None)
        this.percentage = data.get('percentage', None)
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()
        return json.dumps({'success' : True})

    @expose()
    def save_edit_tbl_loader_question_answer(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        if not data: return json.dumps({'success' : False})
        usernow = request.identity['user']
        this = self.get_tbl_loader_question_answer_by_id(**data)
        if not this: return json.dumps({'success' : False})
        this.loader_question_id = data.get('loader_question_id', None)
        this.answer_text = data.get('answer_text', None)
        this.amount = data.get('amount', None)
        this.percentage = data.get('percentage', None)
        if not data.get('active', None): this.active = False
        DBSession.flush()
        return json.dumps({'success' : True})

    @expose()
    def get_tbl_loader_question_answer_by_id(self, *args, **kwargs):
        return DBSession.query(LoaderQuestionAnswer). \
            filter(LoaderQuestionAnswer.id==kwargs.get('tbl_loader_question_answer_id', None)). \
            first()

    @expose()
    def get_active_tbl_loader_question_answer_list(self, *args, **kwargs):
        searchphrase = kwargs.get('searchphrase', None)

        tbl_loader_question_answer_loader_question_id = kwargs.get('tbl_loader_question_answer_loader_question_id', None)
        answer_text = kwargs.get('answer_text', None)
        amount = kwargs.get('amount', None)
        percentage = kwargs.get('percentage', None)

        if tbl_loader_question_answer_loader_question_id:
            dbase_query = DBSession.query(LoaderQuestionAnswer). \
		    filter(LoaderQuestionAnswer.tbl_loader_question_answer_loader_question_id==tbl_loader_question_answer_loader_question_id). \
                        filter(LoaderQuestionAnswer.active==1). \
		    order_by(asc(LoaderQuestionAnswer.tbl_loader_question_answer_id)).limit(LIMIT)
        if answer_text:
            searchphrase = "%"+kwargs['answer_text']+"%"
            dbase_query = DBSession.query(LoaderQuestionAnswer). \
			filter(LoaderQuestionAnswer.answer_text.like(searchphrase)). \
                        filter(LoaderQuestionAnswer.active==1). \
			order_by(asc(LoaderQuestionAnswer.answer_text)).limit(LIMIT)
        if amount:
            searchphrase = "%"+kwargs['amount']+"%"
            dbase_query = DBSession.query(LoaderQuestionAnswer). \
			filter(LoaderQuestionAnswer.amount.like(searchphrase)). \
                        filter(LoaderQuestionAnswer.active==1). \
			order_by(asc(LoaderQuestionAnswer.amount)).limit(LIMIT)
        if percentage:
            searchphrase = "%"+kwargs['percentage']+"%"
            dbase_query = DBSession.query(LoaderQuestionAnswer). \
			filter(LoaderQuestionAnswer.percentage.like(searchphrase)). \
                        filter(LoaderQuestionAnswer.active==1). \
			order_by(asc(LoaderQuestionAnswer.percentage)).limit(LIMIT)
        else:
            dbase_query = DBSession.query(LoaderQuestionAnswer). \
                filter(LoaderQuestionAnswer.active==1). \
                order_by(asc(LoaderQuestionAnswer.id)). \
                limit(LIMIT)
        return dbase_query
