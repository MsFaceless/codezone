# -*- coding: utf-8 -*-
"""Error controller"""
from tg import request, expose, redirect
from rocket.lib.base import BaseController
from rocket.lib.utils import wrap_master, is_user

__all__ = ['ErrorController']


class ErrorController(BaseController):
    """
    Generates error documents as and when they are required.

    The ErrorDocuments middleware forwards to ErrorController when error
    related status codes are returned from the application.

    This behaviour can be altered by changing the parameters to the
    ErrorDocuments middleware in your config/middleware.py file.

    """

    @expose('rocket.templates.error')
    def document(self, *args, **kwargs):
        print("I am be errored")
        """Render the error document"""
        resp = request.environ.get('tg.original_response')
        try:
            # tg.abort exposes the message as .detail in response
            message = resp.detail
        except:
            message = None

        if not message:
            message = ("We're sorry but we weren't able to process "
                       " this request.")

        values = dict(prefix=request.environ.get('SCRIPT_NAME', ''),
                      code=request.params.get('code', resp.status_int if resp else 400),
                      message=request.params.get('message', message))
        return values

    @expose()
    def document(self, *args, **kwargs):
        user_dict = is_user(request)
        if not user_dict: redirect("/login")
        error_card = """
        <div id='error_card' class="row">
            <div class="col-md-12">
                <div class="card">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-6">
                            <h4 class="card-title">Oops.</h4>
                        </div>
                        <div class="col-md-6 text-right">
                            <a href='/'><button id="create_new_product" class="btn btn-primary ml-auto">Go Home</button></a>
                        </div>
                    </div>
                </div>
                <div class="card-body">
                    <h4>An Error has Occurred.</h4>
                    <h5> Please <button id='reload_button' class='btn'>Refresh</button> the page or <a href="/"><button class='btn'>Return Home</button></a></h5>
                    <h5> Alternatively feel free to contact our <button id='fhankyoubtn' class='btn'>Support Team</button></h5>
                    <img id='fhankyou' src="/img/middle.webp" style="display:none"></img>
                </div>
            </div>
        </div>
        """
        js = """
            $("#sidebar").load('/get_sidebar_html?');
            $("#reload_button").click(function(){
                location.reload();
            });
            $("#fhankyoubtn").click(function(){
                $("#fhankyou").show();
            });
        """
        return wrap_master(title='Error', html=error_card, script=js, request=request)
