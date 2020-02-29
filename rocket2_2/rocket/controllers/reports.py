# -*- coding: utf-8 -*-
"""Report controller module"""
from rocket.lib.xlsx_creator import ExcelWriter
from rocket.lib.tg_generic_reportlab import PDFCreator, Paragraph
from reportlab.platypus import Paragraph
from tg import predicates, require, response
from tg import expose, redirect, validate, flash, url, request, use_wsgi_app
from webob.static import FileApp
from datetime import datetime, date, timedelta
from pkg_resources import resource_filename
from tg import predicates, use_wsgi_app
from tg.i18n import ugettext as _
from tg.i18n import lazy_ugettext as l_

from rocket.model import *
from  rocket.lib.type_utils import TypeDictionary
from sqlalchemy import func, desc, asc

from rocket.lib.tg_utils import *
from rocket.lib.base import BaseController

LIMIT = 20
FILENAME = os.path.abspath(resource_filename('rocket', 'public'))
PUBLIC_DIRNAME = os.path.join(FILENAME)
PDF_DIRNAME = os.path.join(PUBLIC_DIRNAME, 'pdf')
EXCEL_DIRNAME = os.path.join(PUBLIC_DIRNAME, 'excel')

SEARCHKEY_ALLOCATION_TO = 'Allocation_ToDate_SearchKeyword'
SEARCHKEY_ALLOCATION_TYPE = 'Allocation_Type_SearchKeyword'
SEARCHKEY_ALLOCATION_GROUP = 'Allocation_Group_SearchKeyword'
SEARCHKEY_ALLOCATION_FROM = 'Allocation_FromDate_SearchKeyword'
SEARCHKEY_ALLOCATION_PRODUCT = 'Allocation_Product_SearchKeyword'
SEARCHKEY_ALLOCATION_PRODUCT_CLASS = 'Allocation_ProductClass_SearchKeyword'

SEARCHKEY_GLEXTRACT_TO = 'GLExtract_ToDate_SearchKeyword'
SEARCHKEY_GLEXTRACT_GROUP = 'GLExtract_Group_SearchKeyword'
SEARCHKEY_GLEXTRACT_FROM = 'GLExtract_FromDate_SearchKeyword'
SEARCHKEY_GLEXTRACT_PRODUCT_CLASS = 'GLExtract_ProductClass_SearchKeyword'
SEARCHKEY_GLEXTRACT_ALLOCATION_TYPE = 'GLExtract_Allocation_Type_SearchKeyword'
SEARCHKEY_GLEXTRACT_CLAIM_VOUCHER_TYPE = 'GLExtract_Claim_Policy_Type_SearchKeyword'

DEFAULT_TO_DATE = datetime.date(datetime.now() - timedelta(days=1))
DEFAULT_FROM_DATE = DEFAULT_TO_DATE - timedelta(days=30)

TYPEUTIL = TypeDictionary()

class ReportController(BaseController):

    def __init__(self, *args, **kwargs):
        pass

    @require(predicates.not_anonymous())
    @expose('rocket.templates.generic')
    def policy_sales(self, *args, **kwargs):
        html = self.get_active_policy_sales_html(*args, **kwargs)
        javascript = self.get_javascript_policy_sales_onload()
        title = _("Policy Sales")
        return dict(title=title, html=html, javascript=javascript)

    @expose()
    def get_active_policy_sales_html(self, *args, **kwargs):
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-6">
                            <h4 class="card-title">{_('Policy Sales')}</h4>
                        </div>
                    </div>
                    <hr>
                </div>
                <div class="card-body">
                </div>
            </div>
        </div>
        """
        return html

    @expose()
    def get_javascript_policy_sales_onload(self, *args, **kwargs):
        javascript = """
        """
        return javascript

    @require(predicates.not_anonymous())
    @expose('rocket.templates.generic')
    def allocations(self, *args, **kwargs):
        html = self.get_active_allocations_html(*args, **kwargs)
        javascript = self.get_javascript_allocations_onload()
        title = _("Allocations")
        return dict(title=title, html=html, javascript=javascript)

    @expose()
    def get_active_allocations_html(self, *args, **kwargs):
        form = self.get_allocation_form(**kwargs)
        htmltbl = self.get_allocation_htmltbl(**kwargs)
        html = f"""
        <div class="card">
            <div class="card-header">
                <div class="row">
                    <div class="col-md-6">
                    <h4 class="card-title">{_('Allocations Report')}</h4>
                    </div>
                    <div class="col-md-6 text-right">
                        <button id='btn_download_pdf' class="btn btn-primary ml-auto">Download PDF</button>
                        <button id='btn_download_xls' class="btn btn-primary ml-auto">Download Excel</button>
                    </div>
                </div>
                <div class="row d-flex align-items-center">
                    <div id='div_allocation_form' class="col-md-12">
                         {form}
                    </div>
                </div>
            </div>
            <hr>
            <div class="card-body">
                <div id='div_allocation' class="table-responsive">
                 {htmltbl}
                </div>
            </div>
        </div>
        """
        return html
    @expose()
    def get_allocation_form(self, *args, **kwargs):
        dropdown_policy_type = self.get_selectbox_policy()
        dropdown_product_class = self.get_selectbox_product_class()
        html = f"""
            <div class="d-flex align-items-center">
                <label class="col-md-2 col-form-label">{_('From Date')}</label>
                <input type="text" name='from_date' id='from_date' class="form-control col-md-4 height_40" value=''/>
                <label class="col-md-2 col-form-label">{_('To Date')}</label>
                <input type="text" name='to_date' id='to_date' class="form-control col-md-4 height_40" value=''/>
            </div>
            <div>
            <div class="d-flex align-items-center mt-2">
                <label class="col-md-2 col-form-label">{_('Policy Type')}</label>
                {dropdown_policy_type}
                <label class="col-md-2 col-form-label">{_('Product Class Type')}</label>
                {dropdown_product_class}
            </div>
            <div class="d-flex align-items-center">
                <button id='btn_search' class="btn btn-primary action_search ml-auto">{_('Search')}</button>
                <button id='btn_reset' class="btn btn-primary">{_('Reset')}</button>
            </div>
        """
        javascript = """
          	"""
        return html + javascript

    @expose()
    def get_allocation_htmltbl(self, *args, **kwargs):
        outputlist = []
        dbase_query = self.get_active_allocations_list(**kwargs)
        for item in dbase_query:
            name = item.get('name', None)
            alloc_type = item.get('alloc_type', None)
            count = item.get('count', 0)
            amount = item.get('amount', 0)
            outputlist.append({
                'allocation' : name,
                'type' : alloc_type,
                'count' : count,
                'amount' : getcurrency(amount),
            })
        dbcolumnlist = [
                'allocation',
                'type',
                'count',
                'amount',
                ]
        theadlist = [
            'Allocation',
            'Type',
            'Count',
            'Amount'
        ]
        tdclasslist = [
            '',
            '',
            'text-center',
            'text-right',
        ]
        return build_html_table(outputlist, dbcolumnlist, theadlist, 'allocationstable', tdclasslist)

    @expose()
    def get_javascript_allocations_onload(self, *args, **kwargs):
        javascript = """
        createDatepicker('#from_date');
        createDatepicker('#to_date');

        exportFile('#btn_download_pdf', '/reports/download_allocations?ext=pdf', focus=false);
        exportFile('#btn_download_xls', '/reports/download_allocations?ext=xls', focus=false);

        $('#btn_search').click(function(){
            var kwargs = 'to_date='+$('#to_date').val();
            kwargs += '&from_date='+$('#from_date').val();
            $('#div_allocation').load('/reports/get_allocation_htmltbl', kwargs, function(data){
                return false;
            });
        })
        $('#btn_reset').click(function(){
        })
        """
        return javascript

    @expose()
    def download_allocations(self, *args, **kwargs):
        ext = kwargs.get('ext', None)
        if ext == 'pdf':
            filename, filepath = self.export_allocation_pdf()
            response.headers["Content-Type"] = 'application/pdf'

        if ext == 'xls':
            filename, filepath = self.export_allocation_xls()
            response.headers["Content-Type"] = 'application/vnd.ms-excel'

        response.headers["Content-Disposition"] = 'attachment; filename="' + filename + '"'
        filecontent = FileApp(filepath)
        return use_wsgi_app(filecontent)

    def export_allocation_pdf(self, *args, **kwargs):
        datename = str(datetime.now()).split(' ')[0]
        filename = f"Allocations {datename}.pdf"
        filepath = os.path.join(PDF_DIRNAME, filename)
        pdffile = PDFCreator(**{'filename':filepath})
        headers=[
                'Allocation',
                'Type',
                'Count',
                'Amount',
                ]
        headerwidths=[
                180,
                180,
                180,
                180,
                ]
        outputlist = []
        dbase_query = self.get_active_allocations_list(**kwargs)
        for item in dbase_query:
            name = item.get('name', None)
            alloc_type = item.get('alloc_type', None)
            count = item.get('count', 0)
            amount = item.get('amount', 0.00)
            outputlist.append((
                Paragraph(str(name), pdffile.styleNormal),
                Paragraph(str(alloc_type), pdffile.styleNormal),
                Paragraph(str(count), pdffile.styleNormal),
                Paragraph(str(getcurrency(amount)), pdffile.styleNormal),
            ))

        product = Product.get_newest()
        print(product)
        userdata = {
            'header':'Allocation Report',
            'title1_header': 'Product Code', 'title1_content': 'Title1 Content',
            'title2_header': 'Title2', 'title2_content': 'Title2 Content',
            'left1_header': 'Left1', 'left1_content': 'Left1 Content',
            'left2_header': 'Left2', 'left2_content': 'Left2 Content',
            'left3_header': 'Left3', 'left3_content': 'Left3 Content',
            'left4_header': 'Left4', 'left4_content': 'Left4 Content',
            'right1_header': 'Right1', 'right1_content': 'Right1 Content',
            'right2_header': 'Right2', 'right2_content': 'Right2 Content',
            'right3_header': 'Right3', 'right3_content': 'Right3 Content',
            'right4_header': 'Right4', 'right4_content': 'Right4 Content',
        }
        pdffile.CreatePDF_Table_Landscape(userdata, outputlist, headers, headerwidths)
        return filename, filepath

    def export_allocation_xls(self, *args, **kwargs):
        datename = str(datetime.now()).split(' ')[0]
        filename = f"Allocations {datename}.xlsx"
        filepath = os.path.join(EXCEL_DIRNAME, filename)
        headers=[
                'Allocation',
                'Type',
                'Count',
                'Amount',
                ]
        outputlist = []
        dbase_query = self.get_active_allocations_list(**kwargs)
        for item in dbase_query:
            name = item.get('name', None)
            alloc_type = item.get('alloc_type', None)
            count = item.get('count', 0)
            amount = item.get('amount', 0.00)
            outputlist.append({
                'allocation' : name,
                'type' : alloc_type,
                'count' : count,
                'amount' : amount,
            })
        userdata = {
            'filepath':filepath,
            'headers':headers,
            'records':outputlist,
        }
        writer = ExcelWriter(**userdata)
        result = writer.generate_file()
        return filename, filepath

    def get_price_from_product_id(self, product_id=None, *args, **kwargs):
        if not product_id: return 0.00

        #rate_table = TYPEUTIL.get_id_of_name('product_price_initial_setup_type', 'rate_table')
        #select_premium = TYPEUTIL.get_id_of_name('product_price_initial_setup_type', 'select_premium')
        #select_sum_assured = TYPEUTIL.get_id_of_name('product_price_initial_setup_type', 'select_sum_assured')
        #fixed_premium_and_sum_assured = TYPEUTIL.get_id_of_name('product_price_initial_setup_type', 'fixed_premium_and_sum_assured')
        product = Product.by_id(product_id)

        fixed_premium = TYPEUTIL.get_id_of_name('product_price_initial_setup_type', 'fixed_premium')
        if product.product_price_initial_setup_type_id == fixed_premium:
            price = ProductPrice.by_attr_first('product_id', product_id)
            if price and price.price:
                return price.price

        fixed_sum_assured = TYPEUTIL.get_id_of_name('product_price_initial_setup_type', 'fixed_sum_assured')
        if product.product_price_initial_setup_type_id == fixed_sum_assured:
            sum_assured = ProductSumAssured.by_attr_first('product_id', product_id)
            if sum_assured and sum_assured.sum_assured:
                return sum_assured.sum_assured

        return 0.00

    def create_transactions(self, *args, **kwargs):

        # Allocation Type
        purchase = TYPEUTIL.get_id_of_name('product_allocation_type', 'purchase')
        acquisition = TYPEUTIL.get_id_of_name('product_allocation_type', 'acquisition')

        # Transaction Type
        executed = TYPEUTIL.get_id_of_name('transaction_extract_status_type', 'executed')

        # Allocation Calc Type
        amount = TYPEUTIL.get_id_of_name('product_allocation_calculation_type', 'amount')
        factor = TYPEUTIL.get_id_of_name('product_allocation_calculation_type', 'factor')
        percentage = TYPEUTIL.get_id_of_name('product_allocation_calculation_type', 'percentage')

        policylist = Policy.get_all('id')
        for pol in policylist:

            alloclinks = BenefitAllocationLink.by_attr_all('product_id', pol.product_id)
            if not alloclinks: continue

            price = self.get_price_from_product_id(pol.product_id)
            for alloc in alloclinks:
                if alloc.product_allocation_type_id == purchase \
                or alloc.product_allocation_type_id == acquisition:

                    exists = DBSession.query(Transaction). \
                            filter(Transaction.policy_id==pol.id). \
                            filter(Transaction.transaction_extract_status_type_id==executed). \
                            filter(Transaction.general_ledger_account_id==alloc.gl_account_id). \
                            first()
                    if not exists:
                        print('Creating Transactions for --->', pol.id, alloc.id)

                        if alloc.product_allocation_calculation_type_id == amount:
                            link = BenefitAllocationLinkCalculationAmount.by_attr_first('product_allocation_link_id', alloc.id)
                            transaction_amount = link.amount

                        elif alloc.product_allocation_calculation_type_id == factor:
                            link = BenefitAllocationLinkCalculationFactor.by_attr_first('product_allocation_link_id', alloc.id)
                            transaction_amount = price * link.factor

                        elif alloc.product_allocation_calculation_type_id == percentage:
                            link = BenefitAllocationLinkCalculationPercentage.by_attr_first('product_allocation_link_id', alloc.id)
                            transaction_amount = (link.percentage/100) * price

                        else:
                            transaction_amount = None

                        if transaction_amount:
                            new = Transaction()
                            new.policy_id = pol.id
                            new.transaction_extract_status_type_id = executed
                            new.amount = transaction_amount
                            new.general_ledger_account_id = alloc.gl_account_id
                            new.added_by = 1
                            DBSession.add(new)
                            DBSession.flush()

                            link = TransactionBenefitAllocationLink()
                            link.transaction_id = new.id
                            link.product_allocation_link_id = alloc.id
                            link.added_by = 1
                            DBSession.add(link)
                            DBSession.flush()

    def get_active_allocations_list(self, *args, **kwargs):
        reset = kwargs.get('reset', None)
        usernow = request.identity.get('user')

        to_date = kwargs.get('to_date', None)
        group_id = kwargs.get('group_id', None)
        from_date = kwargs.get('from_date', None)
        product_id = kwargs.get('product_id', None)
        product_class_id = kwargs.get('product_class_id', None)
        allocation_type_id = kwargs.get('allocation_type_id', None)

        #if not from_date: from_date = datetime.now()
        #if not to_date: to_date = datetime.now()

        #if reset:
        #    COMMON.delete_session_value(SEARCHKEY_ALLOCATION_TO)
        #    COMMON.delete_session_value(SEARCHKEY_ALLOCATION_FROM)
        #    COMMON.delete_session_value(SEARCHKEY_ALLOCATION_TYPE)
        #    COMMON.delete_session_value(SEARCHKEY_ALLOCATION_GROUP)
        #    COMMON.delete_session_value(SEARCHKEY_ALLOCATION_PRODUCT)
        #    COMMON.delete_session_value(SEARCHKEY_ALLOCATION_PRODUCT_CLASS)

        #searchto = COMMON.get_searchphrase(**{'searchkey' : SEARCHKEY_ALLOCATION_TO, 'searchphrase' : to_date})
        #searchfrom = COMMON.get_searchphrase(**{'searchkey' : SEARCHKEY_ALLOCATION_FROM, 'searchphrase' : from_date})
        #search_alloc_type = COMMON.get_searchphrase(**{'searchkey' : SEARCHKEY_ALLOCATION_TYPE, 'searchphrase' : allocation_type_id})
        #search_group = COMMON.get_searchphrase(**{'searchkey' : SEARCHKEY_ALLOCATION_GROUP, 'searchphrase' : group_id})
        #
        #  = COMMON.get_searchphrase(**{'searchkey' : SEARCHKEY_ALLOCATION_PRODUCT, 'searchphrase' : product_id})
        #search_product_class = COMMON.get_searchphrase(**{'searchkey' : SEARCHKEY_ALLOCATION_PRODUCT_CLASS, 'searchphrase' : product_class_id})

        #to_date = date_to_end_datetime(sane_date(searchto) if searchto and not reset else DEFAULT_TO_DATE)
        #from_date = date_to_start_datetime(sane_date(searchfrom) if searchfrom and not reset else DEFAULT_FROM_DATE)

        #product_id = search_product_id if search_product_id and not reset else None
        #allocation_type_id = search_alloc_type if search_alloc_type and not reset else None
        #product_class_id = search_product_class if search_product_class and not reset else None
        #group_id = search_group if search_group and not reset else None

        # Should be in dbase_query below
        #filter(Transaction.registered_date>=from_date). \
        #filter(Transaction.registered_date<=to_date). \

        #self.create_transactions()
        outputlist = []

        alloctypes = TYPEUTIL.get_dict_of_types('product_allocation_type')
        alloclist = BenefitAllocation.get_all('name')
        for alloc in alloclist:
            pretty_name = None

            for id, name in alloctypes.items():
                pretty_name = TYPEUTIL.get_pretty_name('product_allocation_type', id)

                count, amount = 0, 0
                linklist = DBSession.query(BenefitAllocationLink). \
                        filter(BenefitAllocationLink.product_allocation_id==alloc.id). \
                        filter(BenefitAllocationLink.product_allocation_type_id==id). \
                        all()
                for link in linklist:
                    translist = TransactionBenefitAllocationLink.by_attr_all('product_allocation_link_id', link.id)
                    for tr in translist:
                        trans = Transaction.by_id(tr.transaction_id)
                        count += 1
                        amount += trans.amount

                if pretty_name and count and amount:
                    outputlist.append({
                        'name' : alloc.name,
                        'alloc_type' : pretty_name,
                        'count' : count,
                        'amount' : float(amount),
                    })

        return outputlist

        dbase_query = DBSession.query( \
                    BenefitAllocation.name, \
                    BenefitAllocationLink.product_allocation_type_id, \
                    func.count(Transaction.id),  \
                    func.sum(Transaction.amount) \
                ). \
                join(BenefitAllocation, BenefitAllocation.id == BenefitAllocationLink.product_allocation_id). \
                join(TransactionBenefitAllocationLink, TransactionBenefitAllocationLink.product_allocation_link_id == BenefitAllocationLink.id). \
                join(Transaction, Transaction.id == TransactionBenefitAllocationLink.transaction_id). \
                join(Product, Product.id == BenefitAllocationLink.product_id). \
                filter(Transaction.active==True)

        if product_id:
            dbase_query = dbase_query.filter(BenefitAllocation.product_id==product_id)

        if allocation_type_id:
            dbase_query = dbase_query.filter(BenefitAllocation.allocation_type_id==allocation_type_id)

        if product_class_id:
            dbase_query = dbase_query.filter(Product.product_class_id==product_class_id)

        #Greyed out becuase we do not have Group ID on the user object yet!
        #if usernow.group_id:
        #    dbase_query = dbase_query.filter(Product.group_id==usernow.group_id)

        #elif not usernow.group_id and group_id:
        #    dbase_query = dbase_query.filter(Product.group_id==group_id)

        dbase_query = dbase_query. \
                group_by(BenefitAllocationLink.product_allocation_type_id, BenefitAllocation.id). \
                all()
        return dbase_query

    def get_active_transaction_allocations_list(self, *args, **kwargs):
        datename = str(datetime.now()).split(' ')[0]
        filename = f"Allocations {datename}.xlsx"
        filepath = os.path.join(EXCEL_DIRNAME, filename)
        headers=[
                'Allocation',
                'Type',
                'Count',
                'Amount',
                ]
        outputlist = []

        dbase_query = self.get_active_allocations_list(**kwargs)

        for desc, allocation_type_id, count, amount in dbase_query:
            alloc_type = get_name_from_id(AllocationType, allocation_type_id)
            outputlist.append({
                'allocation' : desc,
                'type' : alloc_type,
                'count' : count,
                'amount' : amount,
            })

        userdata = {
            'filepath':filepath,
            'headers':headers,
            'records':outputlist,
        }
        writer = ExcelWriter(**userdata)
        result = writer.generate_file()
        return filename, filepath

    @require(predicates.not_anonymous())
    @expose('rocket.templates.generic')
    def glaccounts(self, *args, **kwargs):
        html = self.get_active_glaccounts_html(*args, **kwargs)
        javascript = self.get_javascript_glaccounts_onload()
        title = _("GL Account Extract")
        return dict(title=title, html=html, javascript=javascript)

    @expose()
    def get_active_glaccounts_html(self, *args, **kwargs):
        form = self.get_glaccount_form(**kwargs)
        htmltbl = self.get_glaccount_htmltbl(**kwargs)
        html = f"""
           <div class="card">
               <div class="card-header">
                   <div class="row">
                       <div class="col-md-6">
                       <h4 class="card-title">{_('GL Account Extract')}</h4>
                       </div>
                       <div class="col-md-6 text-right">
                           <button id='btn_download_pdf' class="btn btn-primary ml-auto">Download PDF</button>
                           <button id='btn_download_xls' class="btn btn-primary ml-auto">Download Excel</button>
                       </div>
                   </div>
                   <div class="row d-flex align-items-center">
                       <div id='div_allocation_form' class="col-md-12">
                            {form}
                       </div>
                   </div>
               </div>
               <hr>
               <div class="card-body">
                   <div id='div_allocation' class="table-responsive">
                    {htmltbl}
                   </div>
               </div>
           </div>
           """
        return html

    @expose()
    def get_glaccount_htmltbl(self, *args, **kwargs):
        outputlist = []
        #Query list
        #db_query =[]
        print("Form Inputs",kwargs)

        #***************************** For test purpose
        if kwargs:
            for item in [kwargs]:
                outputlist.append({
                    'from_date': item.get('from_date'),
                    'to_date': item.get('to_date'),
                })
        # *********************************************

        dbcolumnlist = [
           'to_date',
            'from_date',
            'to_date',
            'to_date',
            'to_date',
            'from_date',
            'to_date',
            'to_date',
            'to_date',
            'from_date',
            'to_date',
            'to_date',
        ]
        theadlist = [
            'Claim',
            'Product',
            'Allocation',
            'Description',
            'Dr Account',
            'Cr Account',
            'Key',
            'Type',
            'Count',
            'Amount',
            'Distribution',
            'Price'
        ]
        tdclasslist = [
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            'text-right'
        ]
        return build_html_table(outputlist, dbcolumnlist, theadlist, 'glextracts_table', tdclasslist)

    @expose()
    def get_glaccount_form(self, *args, **kwargs):
        dropdown_policy = self.get_selectbox_policy()
        dropdown_product_class = self.get_selectbox_product_class()
        html = f"""
               <div class="d-flex align-items-center">
                   <label class="col-md-2 col-form-label">{_('From Date')}</label>
                   <input type="text" name='from_date' id='from_date' class="form-control col-md-4 height_40" value=''/>
                   <label class="col-md-2 col-form-label">{_('To Date')}</label>
                   <input type="text" name='to_date' id='to_date' class="form-control col-md-4 height_40" value=''/>
               </div>
               <div>
               <div class="d-flex align-items-center mt-2">
                   <label class="col-md-2 col-form-label">{_('Policy Type')}</label>
                   {dropdown_policy}
                   <label class="col-md-2 col-form-label">{_('Product Class Type')}</label>
                   {dropdown_product_class}
               </div>
               <div class="d-flex align-items-center">
                   <button id='btn_search' class="btn btn-primary action_search ml-auto">{_('Search')}</button>
                   <button id='btn_reset' class="btn btn-primary">{_('Reset')}</button>
               </div>
           """
        javascript = """
             	"""
        return html + javascript

    @expose()
    def get_javascript_glaccounts_onload(self, *args, **kwargs):
        javascript = """
              createDatepicker('#from_date');
              createDatepicker('#to_date');
              exportFile('#btn_download_pdf', '/reports/download_glextract?ext=pdf');
              exportFile('#btn_download_xls', '/reports/download_glextract?ext=xls', focus=false);
                  $('#btn_search').click(function(){
                     var kwargs = 'to_date='+$('#to_date').val();
                     kwargs += '&from_date='+$('#from_date').val();
                     console.log(kwargs);
                     $('#div_allocation').load('/reports/get_glaccount_htmltbl', kwargs, function(data){
                         return false;
                     });
                 })
                 $('#btn_reset').click(function(){
                  console.log('reset options');
                 })
        """
        return javascript

    @expose()
    def download_glextract(self, *args, **kwargs):
        ext = kwargs.get('ext', None)
        if ext == 'pdf':
            filename, filepath = self.export_glextract_pdf()
            response.headers["Content-Type"] = 'application/pdf'

        if ext == 'xls':
            filename, filepath = self.export_glextract_xls()
            response.headers["Content-Type"] = 'application/vnd.ms-excel'

        response.headers["Content-Disposition"] = 'attachment; filename="' + filename + '"'
        filecontent = FileApp(filepath)
        return use_wsgi_app(filecontent)

    def export_glextract_pdf(self, *args, **kwargs):
        datename = str(datetime.now()).split(' ')[0]
        filename = f"General Ledger Extract {datename}.pdf"
        filepath = os.path.join(PDF_DIRNAME, filename)
        pdffile = PDFCreator(**{'filename': filepath})
        headers = [
            'Claim',
            'Product',
            'Allocation',
            'Description',
            'Dr Account',
            'Cr Account',
            'Key',
            'Type',
            'Count',
            'Amount',
            'Distribution',
            'Price'
        ]
        headerwidths = [
            70,
            70,
            70,
            70,
            70,
            70,
            70,
            70,
            70,
            70,
            70,
            70,
        ]
        outputlist = []
        dbase_query =[]

        print()
        print('#TGJ# Insert SQL data collection here.')
        print()

        for item in dbase_query:
            outputlist.append((
                Paragraph(checknullvalue(item), pdffile.styleNormal),
                Paragraph(checknullvalue(item), pdffile.styleNormal),
                Paragraph(checknullvalue(item), pdffile.styleNormal),
                Paragraph(checknullvalue(item), pdffile.styleNormal),
                Paragraph(checknullvalue(item), pdffile.styleNormal),
                Paragraph(checknullvalue(item), pdffile.styleNormal),
                Paragraph(checknullvalue(item), pdffile.styleNormal),
                Paragraph(checknullvalue(item), pdffile.styleNormal),
                Paragraph(checknullvalue(item), pdffile.styleNormal),
                Paragraph(getcurrency(item), pdffile.styleNormal),
                Paragraph("", pdffile.styleNormal),
                Paragraph(getcurrency(item), pdffile.styleNormal),
            ))
        userdata = {
            'header': 'General Ledger Extract Report',
            'right1_header': 'Date Printed', 'right1_content': str(datename),
        }
        pdffile.CreatePDF_Table_Landscape(userdata, outputlist, headers, headerwidths)
        return filename, filepath

    def export_glextract_xls(self, *args, **kwargs):
        datename = str(datetime.now()).split(' ')[0]
        filename = f"General Ledger Account {datename}.xlsx"
        filepath = os.path.join(EXCEL_DIRNAME, filename)
        headers = [
            'Claim',
            'Product',
            'Allocation',
            'Description',
            'Dr Account',
            'Cr Account',
            'Key',
            'Type',
            'Count',
            'Amount',
            'Distribution',
            'Price'
        ]
        outputlist = []
        dbase_query =[]
        for claim_id, code, alloc_desc, gl_desc, dr_account, cr_account, gl_key, count, amount, allocation_type_id, price in dbase_query:
            outputlist.append({
                'claim_id': claim_id,
                'product_code': code,
                'alloc_description': alloc_desc,
                'description': gl_desc,
                'dr_account': dr_account,
                'cr_account': cr_account,
                'gl_key': gl_key,
                'type': "",
                'count': count,
                'amount': getcurrency(amount),
                'distribution': "",
                'price': getcurrency(price),
            })
        userdata = {
            'filepath': filepath,
            'headers': headers,
            'records': outputlist,
        }
        writer = ExcelWriter(**userdata)
        result = writer.generate_file()
        return filename, filepath


    def get_selectbox_product_class(self, *args, **kwargs):
        kwargs['id'] = 'product_type_id'
        kwargs['outputdict'] = TYPEUTIL.get_dict_of_types("product_type")
        return create_selectbox_html(**kwargs)

    def get_selectbox_policy(self, *args, **kwargs):
        kwargs['id'] = 'policy_type_id'
        kwargs['outputdict'] = TYPEUTIL.get_dict_of_types("policy_type")
        return create_selectbox_html(**kwargs)
