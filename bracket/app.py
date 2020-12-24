# -*- coding: utf-8 -*-
"""
    bracket
    ~~~~~

    Bracket is an Elegant static site generator.

    :copyright: (c) 2020 by Ceorleorn(https://github.com/ceorleorn).
    :license: MIT License, see LICENSE for more details.
"""
from .context import PagesContext
import importlib

class WebSite(object):
    def __init__(self, import_name, import_modules={}):
        self.import_name = import_name
        self.import_modules = import_modules

        self.pages_list = []
        self.resources_list = []
    
    def add_page(self,rule,viewfunc):
        if not rule.startswith("/"):
            raise ValueError("The route must start with a forward slash.")

        self.pages_list.append({
            "rule":rule,
            "viewfunc":viewfunc
        })
    
    def add_resource(self,func):
        self.resources_list.append(func)
    
    def pages(self, rule):
        def decorator(f):
            self.add_page(rule=rule,viewfunc=f)
            return f

        return decorator
    
    def resources(self):
        def decorator(f):
            self.add_resource(func=f)
            return f

        return decorator
    
    def dispatch(self,route):
        for obj in self.pages_list:
            if obj["rule"] == route:
                dispatch = obj["viewfunc"](PagesContext)
                if isinstance(dispatch,PagesContext):
                    return dispatch.render()
                else:
                    return dispatch

        return None
            
        

    def serve(self,serveconfig={
        "port":5000
    }):
        try:
            flask = importlib.import_module("flask")
        except:
            raise RuntimeError("Flask is not installed.")
        
        app = flask.Flask("Bracket",static_url_path="/static")
        
        @app.route("/",methods=["GET","POST"])
        def indexhandler():
            dispatch = self.dispatch("/")
            if not (dispatch == None):
                return dispatch
            else:
                return flask.abort(404)

        @app.route("/<url>",methods=["GET","POST"])
        def otherurlhandler(url):
            dispatch = self.dispatch("/" + url)
            if not (dispatch == None):
                return dispatch
            else:
                return flask.abort(404)
        
        app.run(port=serveconfig["port"])
