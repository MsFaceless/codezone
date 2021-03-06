#class_name = Member
#table_name = tbl_member
#prefix =PRE
#postfix =POST
#columns_to_create = [id, person_id, register_date, external_id] #id - primary_key autoincrement=True
#cont_name = members
#html_template_name = generic
#dbsession = DBSession
#controller_name = MemberController
#view_cols_list = [person_id, register_date, external_id]
#search_cols_list = [person_id, register_date, external_id]
#pdf_cols_list = [person_id, register_date, external_id]
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
#class_name = Member
#table_name =tbl_member
#prefix =PRE
#postfix =POST
#columns_to_create = [id, person_id, register_date, external_id] #id - primary_key autoincrement=True
#cont_name =members
#html_template_name =generic
#dbsession =DBSession
#controller_name =MemberController
#view_cols_list = [person_id, register_date, external_id]
#search_cols_list = [person_id, register_date, external_id]
#pdf_cols_list = [person_id, register_date, external_id]
#link_to_id_or_None =
#link_class_name_None =

############################
# Controller
############################


class MemberController(BaseController):
    """Docstring for members."""

    def __init__(self, *args, **kwargs):
        pass

    @require(predicates.not_anonymous())
    @expose('rocket_app.templates.generic')
    def tbl_members(self, *args, **kwargs):
        html = self.get_active_tbl_member_html(*args, **kwargs)
        javascript = self.get_javascript_tbl_member_onload()
        title = "Member"
        return dict(title=title, html=html, javascript=javascript)

    @expose()
    def get_active_tbl_member_html(self, *args, **kwargs):
        usernow = request.identity['user']
        dbase_query = self.get_active_tbl_member_list(*args, **kwargs)
        outputlist = []
        for item in dbase_query:
            outputlist.append({
                'person_id' : "<div class='edit tbl_member_edit' tbl_member_id='{1}'>{0}</div>".format(item.person_id, item.id),
                'register_date' : item.register_date,
                'external_id' : item.external_id,
                             })
        dbcolumnlist=[
                'person_id',
                'register_date',
                'external_id',
                    ]
        theadlist=[
                'Person_Id',
                'Register_Date',
                'External_Id',
                ]
        tbl_membertable = build_html_table(outputlist, dbcolumnlist, theadlist, "tbl_member_table")
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-6">
                            <h4 class="card-title">Member</h4>
                        </div>
                        <div class="col-md-6 text-right">
                            <button id="create_new_tbl_member" class="btn btn-primary ml-auto">Create a new Member</button>
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
                        {tbl_membertable}
                    </div>
                </div>
                </div>
            </div>
        """
        return html

    @expose()
    def get_javascript_tbl_member_onload(self, *args, **kwargs):
        javascript = """
        $("#create_new_tbl_member").click(function(){
            $.redirect('/members/new_tbl_member');
        });
        $(".tbl_member_edit").click(function(){
            var data = {tbl_member_id : $(this).attr('tbl_member_id')};
            $.redirect('/members/edit_tbl_member', data);
        });
        """
        return javascript

    @expose('rocket_app.templates.generic')
    def new_tbl_member(self, *args, **kwargs):
        html = """
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-header d-flex">
                        <div class="col-md-6">
                            <h4 class="card-title">New Member</h4>
                        </div>
                        <div class="col-md-6 text-right">
                            <button class="btn btn-primary ml-auto action_back tbl_member_back">Back to Member List</button>
                        </div>
                    </div>
                    <div class="card-body">
                        <form id='form_new_tbl_member'>
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="person_id">Person_Id</label>
						<div class="col-md-9">
							<input id="person_id" type="text" name="person_id" class="form-control" required='true'>
						</div>
					</div>
				</div>
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="register_date">Register_Date</label>
						<div class="col-md-9">
							<input id="register_date" type="text" name="register_date" class="form-control" required='true'>
						</div>
					</div>
				</div>
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="external_id">External_Id</label>
						<div class="col-md-9">
							<input id="external_id" type="text" name="external_id" class="form-control" required='true'>
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
                        <button id='save_new_tbl_member' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary tbl_member_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        setFormValidation('#form_new_tbl_member');
        $("#register_date").datetimepicker({ format: 'DD/MM/YYYY' });
        $('#save_new_tbl_member').click(function(){
             var valid = FormIsValid("#form_new_tbl_member");
             if(valid){
                var formserial = getFormData('#form_new_tbl_member');
                var data = {data : JSON.stringify(formserial)};

                $.post('/members/save_new_tbl_member?', data, function(data){
                    var result = JSON.parse(data);
                    if(result.success === true){
                        $.redirect('/members/tbl_members');
                    };
                    return false;
                });
             }
        });
        $('.tbl_member_back').click(function(){
            $.redirect('/members/tbl_members');
        });
     	"""
        title = "New Member"
        return dict(title=title, html=html, javascript=javascript)

    @expose('rocket_app.templates.generic')
    def edit_tbl_member(self, *args, **kwargs):
        tbl_member_id = kwargs.get('tbl_member_id', None)
        if not tbl_member_id: redirect('/members/tbl_members')
        this = self.get_tbl_member_by_id(*args, **kwargs)
        if not this: redirect('/members/tbl_members')
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-header d-flex">
                        <div class="col-md-6">
                            <h4 class="card-title">Edit Member</h4>
                        </div>
                        <div class="col-md-6 text-right">
                            <button class="btn btn-primary ml-auto action_back tbl_member_back">Back to Member List</button>
                        </div>
                    </div>
                    <div class="card-body">
                        <form id='form_edit_tbl_member'>
                                <div style='display: none' class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="tbl_member_id">Id</label>
						<div class="col-md-9">
							<input id="id" type="text" name="tbl_member_id" value="{this.id}" class="form-control" required='true'>
						</div>
					</div>
				</div>
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="person_id">Person_Id</label>
						<div class="col-md-9">
							<input id="person_id" type="text" name="person_id" value="{this.person_id}" class="form-control" required='true'>
						</div>
					</div>
				</div>
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="register_date">Register_Date</label>
						<div class="col-md-9">
							<input id="register_date" type="text" name="register_date" value="{this.register_date}" class="form-control" required='true'>
						</div>
					</div>
				</div>
                                <div class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="external_id">External_Id</label>
						<div class="col-md-9">
							<input id="external_id" type="text" name="external_id" value="{this.external_id}" class="form-control" required='true'>
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
                        <button id='save_edit_tbl_member' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary tbl_member_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        setFormValidation('#form_edit_tbl_member');
        $("#register_date").datetimepicker({ format: 'DD/MM/YYYY' });
        $('#save_edit_tbl_member').click(function(){
             var valid = FormIsValid("#form_edit_tbl_member");
             if(valid){
                var formserial = getFormData('#form_edit_tbl_member');
                var data = {data : JSON.stringify(formserial)};

                $.post('/members/save_edit_tbl_member?', data, function(data){
                    var result = JSON.parse(data);
                    if(result.success === true){
                        $.redirect('/members/tbl_members');
                    };
                    return false;
                });
             }
        });
        $('.tbl_member_back').click(function(){
            $.redirect('/members/tbl_members');
        });
     	"""
        title = "Edit Member"
        return dict(title=title, html=html, javascript=javascript)

    @expose()
    def save_new_tbl_member(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        if not data: return json.dumps({'success' : False})
        usernow = request.identity['user']
        this = Member()
        this.person_id = data.get('person_id', None)
        this.register_date = data.get('register_date', None)
        this.external_id = data.get('external_id', None)
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()
        return json.dumps({'success' : True})

    @expose()
    def save_edit_tbl_member(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        if not data: return json.dumps({'success' : False})
        usernow = request.identity['user']
        this = self.get_tbl_member_by_id(**data)
        if not this: return json.dumps({'success' : False})
        this.person_id = data.get('person_id', None)
        this.register_date = data.get('register_date', None)
        this.external_id = data.get('external_id', None)
        if not data.get('active', None): this.active = False
        DBSession.flush()
        return json.dumps({'success' : True})

    @expose()
    def get_tbl_member_by_id(self, *args, **kwargs):
        return DBSession.query(Member). \
            filter(Member.id==kwargs.get('tbl_member_id', None)). \
            first()

    @expose()
    def get_active_tbl_member_list(self, *args, **kwargs):
        searchphrase = kwargs.get('searchphrase', None)

        tbl_member_person_id = kwargs.get('tbl_member_person_id', None)
        register_date_start = kwargs.get('register_date_start', None)
        register_date_end = kwargs.get('register_date_end', None)
        tbl_member_external_id = kwargs.get('tbl_member_external_id', None)

        if tbl_member_person_id:
            dbase_query = DBSession.query(Member). \
		    filter(Member.tbl_member_person_id==tbl_member_person_id). \
                        filter(Member.active==1). \
		    order_by(asc(Member.tbl_member_id)).limit(LIMIT)
        if register_date_start:
            if not register_date_end: register_date_end = datetime.date(datetime.now())
            dbase_query = DBSession.query(Member). \
			filter(Member.register_date>=register_date_start). \
			filter(Member.register_date<=register_date_end). \
                        filter(Member.active==1). \
			order_by(asc(Member.id)).limit(LIMIT)
        if tbl_member_external_id:
            dbase_query = DBSession.query(Member). \
		    filter(Member.tbl_member_external_id==tbl_member_external_id). \
                        filter(Member.active==1). \
		    order_by(asc(Member.tbl_member_id)).limit(LIMIT)
        else:
            dbase_query = DBSession.query(Member). \
                filter(Member.active==1). \
                order_by(asc(Member.id)). \
                limit(LIMIT)
        return dbase_query
