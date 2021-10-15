
from flask import Flask, request,jsonify
from flask_restful import Api, Resource, reqparse
from db import DBconfig
from datetime import date
import datetime
import json
import os,time
from werkzeug.utils import secure_filename

from models import Stock


class Stock(Resource):
  def get(self):
    """Get the stock details for using this function

    Arguments
    ---------
    page
        pagination page number

    limit
        how many records showed per page

    Returns
    -------
    json
        a status of function return json format
    """
    
    page = 1
    limit = 10
    
    stocks = stock.objects(status=1).paginate(page=page,per_page=limit)
    if not stocks:
        return jsonify({'error': 'data not found'})
    else:
        return jsonify([u.to_json() for u in stocks.items])

  def post(self):

    """Create the stock for using this function

    Returns
    -------
    json
        a status of function return json format
    """

    stock_flag , email_flag = False , False
    
    stock = request.form #stock form
    
    productname_exist = stock.objects(productname=stock['productname']).first()

    if productname_exist:
        return jsonify({'status': 'failed','messgage':'productname Already exsist, Please try different!.'})
    

    created_at = datetime.datetime.now()
    
    stock = stock(productname = stock['productname'],
                price=stock['price'],
                quantity = stock['quantity'],
                purchase_date = stock['purchase_date'],
                created_at = created_at,
                updated_at = created_at,
                status=1)
    stock.save()

    return jsonify({'status': 'success','messgage':'stock created Successfully!.'})


    def put(self):

        """Update the stock for using this function

        Returns
        -------
        json
            a status of function return json format
        """
        
        stock = request.form
        
        if 'productname' not in stock:
            return jsonify({'error':"productname is must to Edit the data!."})

        record = stock.objects(productname=stock['productname']).first()

        
        if not record:
            return jsonify({'status': 'failed','error': 'stock not found'})
        else:
            
            record.update(updated_at=datetime.datetime.now(), **stock)
            record = stock.objects(productname=stock['productname']).first()
        
        return jsonify({'status': 'success','messgage':'stock data Updated Successfully!.'})


    def delete(self):
        """Deleting the stock for using this function

        Returns
        -------
        json
            a status of function return json format
        """

        
        stock = request.form

        if 'productname' not in stock:
            return jsonify({'error':"productname is Must to Delete the data!."})

        stock = stock.objects(productname=stock['productname']).first()
        if not stock:
            return jsonify({'status': 'failed','error': 'data not found'})
        else:
            stock.update(status=2)
        return jsonify({'status':'success',"message":"stock Deleted Successfully!."})