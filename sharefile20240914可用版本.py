# -*- coding: utf-8 -*-

from flask import Flask, send_from_directory, request, jsonify, render_template_string, abort #Flask==3.0.0
import os
import sys
import random
import pyperclip                                                                       #pyperclip==1.8.2
import winreg
import socket
import psutil                                                                     #psutil==5.9.6
import time
import threading 
import tkinter as tk 
from tkinter import filedialog
from PIL import ImageTk, Image, ImageDraw, ImageFont                             #Pillow==9.2.0
import qrcode                                                                      #qrcode==7.4.2
from colorama import init, Fore, Back, Style                                     #colorama==0.4.6
from datetime import datetime
import shutil
import logging
import zipfile
import tempfile
import pythoncom                                                                    #pywin32==300
from win32com.shell import shell, shellcon

CLSID_ShellLink = shell.CLSID_ShellLink
IID_IShellLink = shell.IID_IShellLink

def start_flask_server(p, fol, cip):
    app = Flask(__name__)
    app.config["UPLOAD_FOLDER"] = fol
    app.config["UPLOAD_TEMP_FOLDER"] = fol
    app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024 * 1024
    
    EXCLUDED_DIRS = {'System Volume Information', '$RECYCLE.BIN', 'RECYCLER', '$Recycle.Bin', 'Recovery'}
    
    logging.getLogger("werkzeug").disabled = True #将 Werkzeug 的日志记录器设置为禁用状态
    
    @app.before_request
    def check_auth():
        client_ip = request.remote_addr

    @app.route('/')
    def index():
        html1 = '''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport"content="width=device-width, initial-scale=1.0"><title>局域网文件传输助手</title><style type="text/css">#mine{margin:5px auto}.level{text-align:center;margin-bottom:10px}.level button{padding:5px 15px;background-color:#02a4ad;border:none;color:#fff;border-radius:3px;outline:none;cursor:pointer}.level button.active{background-color:#00abff}table{border-spacing:1px;background-color:#929196;margin:0 auto}td{padding:0;width:20px;height:20px;background-color:#ccc;border:2px solid;border-color:#fff#a1a1a1#a1a1a1#fff;text-align:center;line-height:20px;font-weight:bold}.tips{color:red;font-size:16px}.mine{background:#d9d9d9 url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAARFJREFUOE+V0r1KA0EUxfHf7orgGwhKEAIW0cbCRhsLSz8qLXwFX0CwsRJfw8IqhWgvpvABbGIloiDWdjaZXY1uYLPZZON0M3Pvf+aecyLDq4WnmLOYTo9O6X5kG1UU/EISdjJWUy4mQcqAVsxByiVe617v31f9oNi3HHOUF3YD7TJ0EmA+4Rbrg6YfwEp/vCKkEhBzEnGM50LxV0Yj5bAIGQEk7OFm3PwZ3SKkCvCAzUkCZpymnFeJ2Eh4m0L9u8D2CGCGrYz7KQBC7mB5hNmET8zVQF4Czcoc5Nbt1gDa4c+NyiA1k2H7yqyPwMLgcFyQlhKusFHsznhMWasNUl7Q12M/YxG9iPfA9X+iPI0ZvgGuQTgRPscqngAAAABJRU5ErkJggg==)no-repeat center;background-size:cover}.flag{background:#ccc url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAALxJREFUOE/tkyEOAjEQRd/4JQFFglrFCfDsLQgCwU3gGmDQCCyGhDUcgVWrOQCshAx0KUmztKE4BDUV8+d1Mr9fsEdprUELkCGQAUegAN0J1eKla97iAPa20ac9gS5toQ8yBp0L1SwW4IH+AZ+WaCzsAZ2QfQGAbICtcC5No5KMQCbAAOg6sNwC8oaNtTW571WlncI1NTVXEw2I/InhCX4coCTZI4UmTCvhMg1b916pl/jc8O1gEmcS9g3gDoHKYhEZ0qyeAAAAAElFTkSuQmCC)no-repeat center;background-size:cover}.info{margin-top:10px;text-align:center}td.zero{background-color:#d9d9d9;border-color:#d9d9d9}td.one{background-color:#d9d9d9;border-color:#d9d9d9;color:#0332fe}td.two{background-color:#d9d9d9;border-color:#d9d9d9;color:#019f02}td.three{background-color:#d9d9d9;border-color:#d9d9d9;color:#ff2600}td.four{background-color:#d9d9d9;border-color:#d9d9d9;color:#93208f}td.five{background-color:#d9d9d9;border-color:#d9d9d9;color:#ff7f29}td.six{background-color:#d9d9d9;border-color:#d9d9d9;color:#ff3fff}td.seven{background-color:#d9d9d9;border-color:#d9d9d9;color:#3fffbf}td.eight{background-color:#d9d9d9;border-color:#d9d9d9;color:#22ee0f}.titl{width:100%;text-align:center;font-size:20px;color:#1296db;margin-bottom:10px}</style></head><body><div id="mine"><div class="titl">欢迎使用局域网文件传输助手<br>放松一下吧</div><div class="level"><button class="active">初级</button><button>中级</button><button>高级</button><button>重新开始</button></div><div class="gameBox"></div><div class="info">剩余雷数：<span class="mineNum"></span><br><span class="tips">左键扫雷，右键插旗，再次点击右键拔旗</span></div></div><script type="text/javascript">function Mine(t,e,s){this.tr=t,this.td=e,this.mineNum=s,this.squares=[],this.tds=[],this.surplusMine=s,this.allRight=!1,this.parent=document.querySelector(".gameBox")}Mine.prototype.randomNum=function(){for(var t=new Array(this.tr*this.td),e=0;e<t.length;e++)t[e]=e;return t.sort(function(){return.5-Math.random()}),t.slice(0,this.mineNum)},Mine.prototype.init=function(){for(var t=this.randomNum(),e=-1,s=0;s<this.tr;s++){this.squares[s]=[];for(var i=0;i<this.td;i++)e++,-1!=t.indexOf(e)?this.squares[s][i]={type:"mine",x:i,y:s}:this.squares[s][i]={type:"number",x:i,y:s,value:0}}this.updateNum(),this.createDom(),this.parent.oncontextmenu=function(){return!1},this.mineNumDom=document.querySelector(".mineNum"),this.mineNumDom.innerHTML=this.surplusMine},Mine.prototype.createDom=function(){for(var t=this,e=document.createElement("table"),s=0;s<this.tr;s++){var i=document.createElement("tr");this.tds[s]=[];for(var n=0;n<this.td;n++){var r=document.createElement("td");this.tds[s][n]=r,r.pos=[s,n],r.onmousedown=function(){t.play(event,this)},i.appendChild(r)}e.appendChild(i)}this.parent.innerHTML="",this.parent.appendChild(e)},Mine.prototype.getAround=function(t){for(var e=t.x,s=t.y,i=[],n=e-1;n<=e+1;n++)for(var r=s-1;r<=s+1;r++)n<0||r<0||n>this.td-1||r>this.tr-1||n==e&&r==s||"mine"==this.squares[r][n].type||i.push([r,n]);return i},Mine.prototype.updateNum=function(){for(var t=0;t<this.tr;t++)for(var e=0;e<this.td;e++)if("number"!=this.squares[t][e].type)for(var s=this.getAround(this.squares[t][e]),i=0;i<s.length;i++)this.squares[s[i][0]][s[i][1]].value+=1},Mine.prototype.play=function(t,e){var s=this;if(1==t.which&&"flag"!=e.className){var n=this.squares[e.pos[0]][e.pos[1]],r=["zero","one","two","three","four","five","six","seven","eight"];if("number"==n.type){if(e.innerHTML=n.value,e.className=r[n.value],0==n.value){e.innerHTML="",function t(e){for(var i=s.getAround(e),n=0;n<i.length;n++){var a=i[n][0],o=i[n][1];s.tds[a][o].className=r[s.squares[a][o].value],0==s.squares[a][o].value?s.tds[a][o].check||(s.tds[a][o].check=!0,t(s.squares[a][o])):s.tds[a][o].innerHTML=s.squares[a][o].value}}(n)}}else this.gameOver(e)}if(3==t.which){if(e.className&&"flag"!=e.className)return;if(e.className="flag"==e.className?"":"flag","mine"==this.squares[e.pos[0]][e.pos[1]].type?this.allRight=!0:this.allRight=!1,"flag"==e.className?this.mineNumDom.innerHTML=--this.surplusMine:this.mineNumDom.innerHTML=++this.surplusMine,0==this.surplusMine)if(1==this.allRight)for(alert("恭喜你，游戏通过"),i=0;i<this.tr;i++)for(j=0;j<this.td;j++)this.tds[i][j].onmousedown=null;else alert("游戏失败"),this.gameOver()}},Mine.prototype.gameOver=function(t){for(i=0;i<this.tr;i++)for(j=0;j<this.td;j++)"mine"==this.squares[i][j].type&&(this.tds[i][j].className="mine"),this.tds[i][j].onmousedown=null;t&&(t.style.backgroundColor="#f00")};var btns=document.getElementsByTagName("button"),mine=null,ln=0,arr=[[9,9,10],[16,16,40],[16,30,99]];for(let t=0;t<btns.length-1;t++)btns[t].onclick=function(){btns[ln].className="",this.className="active",(mine=new Mine(arr[t][0],arr[t][1],arr[t][2])).init(),ln=t};btns[0].onclick(),btns[3].onclick=function(){for(var t=0;t<btns.length-1;t++)"active"==btns[t].className&&btns[t].onclick()};	</script></body></html>'''
        html2 = '''<!doctype html><html lang="en"><head><meta charset="UTF-8"><meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" /><meta name="viewport" content="width=540,user-scalable=no"><title>黑白棋</title><style type="text/css">body{background:#c4824d;font-family:"微软雅黑","黑体",serif;margin:0;padding:0}#desk{width:750px;margin:0px auto}#title{float:left;width:60px;padding:15px}#console{float:left;width:110px;padding:10px 0px 0px 10px}h1{margin:10px 0px;color:black;font-size:60px;line-height:70px;font-weight:bold;text-shadow:0px 0px 6px #A33D1B,0px 7px 3px #754B35}h1 span{color:white}.button{margin:15px 0px;width:100px;height:58px;font-size:30px;line-height:58px;color:#440000;background:#dd8e4f;border:1px solid #ff6600;border-radius:30px;box-shadow:0px 4px 10px #482915;text-align:center;cursor:default}.button:hover{background:#E4A774;border:1px solid #ff3300;box-shadow:0px 6px 10px #482915}.button:active{color:#600;background:#eec7a6;border:1px solid #ff0000;box-shadow:0px 2px 5px #482915;position:relative;top:2px}.cbox{border:3px solid transparent;border-radius:10px;width:100px;height:56px}.side{border:3px solid #cc3333;background:#DBA977}.cbox span{float:right;font-size:30px;line-height:54px;font-weight:bold;color:#500;text-shadow:0px 0px 3px #E8C488;padding-right:7px}#interface{position:relative;float:left;width:540px;height:560px}#chessboard{width:522px;height:522px;margin:15px 7px;border:2px solid #CA521E;background:#51150b;box-shadow:0px 8px 15px #482915;-webkit-transform:perspective(740px) rotateX(0deg);transform:perspective(740px) rotateX(0deg);-webkit-transition:-webkit-transform 1s;transition:transform 1s}#chessboard table{background:#835f2e;border-spacing:2px;border:20px solid #51150b}#chessboard td{width:54px;height:54px;border:1px solid #e4c8a9}#chessboard td:hover{border:1px solid #f00}#chessboard .bg0{background:#c1914f}#chessboard .bg1{background:#cba470}.black,.white{width:10px;height:10px;border-radius:50%;margin:5px;padding:17px;box-shadow:0px 4px 10px #482915}.black{background:black;-webkit-transform:rotateY(0deg);transform:rotateY(0deg)}.white{background:white;-webkit-transform:rotateY(180deg);transform:rotateY(180deg)}.reversal{-webkit-transition:-webkit-transform 400ms ease-in-out,background 0ms 200ms;transition:transform 400ms ease-in-out,background 0ms 200ms}.newest:before,.reversal:before{content:"";display:block;width:10px;height:10px;border-radius:5px}.newest:before{background:#f00}.reversal:before{background:#66c}.prompt{width:14px;height:14px;border-radius:50%;margin:20px;padding:0px;background:#FFCC33}#buttons{margin:0px 40px}#buttons div{float:left;margin:0px 10px}#pass,#airuning{position:absolute;top:12px;left:50%;margin-left:-150px;width:300px;height:auto;border-radius:13px;text-align:center;font-size:18px;line-height:26px;background:rgba(230,160,80,0.6);color:#330000;text-shadow:0px 0px 3px #900;display:none}#airuning{top:520px;margin-left:-100px;width:200px}#winner{position:absolute;margin:0 auto;width:100%;height:50px;top:255px;text-align:center;display:none;color:#f20c00;line-height:50px;font-size:30px;background:rgba(230,160,80,0.6);border-radius:25px}@media screen and (max-width:750px){#desk{width:540px}#title{width:100%;padding:0px;text-align:center}#console{width:96%;padding:10px 2%}h1{display:inline-block}.cbox{float:left}#console .button{float:left;margin:0px 5px;width:90px}}</style></head><body><div id="desk"><div id="title"><h1>黑<span>白</span>棋</h1></div><div id="interface"><div id="chessboard"></div><div id="pass"></div><div id="airuning">计算中……</div><div id="winner"></div></div><div id="console"><div id="side1"class="cbox"><span>0</span><div class="black"></div></div><div id="side2"class="cbox"><span>0</span><div class="white"></div></div><div id="play"class="button">开始</div><div id="back"class="button">悔棋</div></div></div><script type="text/javascript">"use strict";function Chessboard(){var e,n,t,a=this;a.toDown=null,a.create=function(){for(var s=document.getElementById("chessboard"),o="<table>",c=0;c<8;c++){o+="<tr>";for(var l=0;l<8;l++)o+="<td class='bg"+(l+c)%2+"'><div></div></td>";o+="</tr>"}o+="</table>",s.innerHTML=o,e=s.getElementsByTagName("div"),function(n){for(var t=0;t<64;t++)!function(t){n[t].onclick=function(){"prompt"==e[t].className&&a.toDown(t)}}(t);n=void 0}(s.getElementsByTagName("td")),n=document.getElementById("console").getElementsByTagName("span"),t={1:document.getElementById("side1"),"-1":document.getElementById("side2")}},a.update=function(a,s){for(var o=0;o<64;o++)e[o].className=["white","","black"][a[o]+1];if(!s)for(var c in a.next)e[c].className="prompt";for(o=0;o<a.newRev.length;o++)e[a.newRev[o]].className+=" reversal";-1!=a.newPos&&(e[a.newPos].className+=" newest"),n[0].innerHTML=a.black,n[1].innerHTML=a.white,t[a.side].className="cbox side",t[-a.side].className="cbox"}}function AI(){var e=this;e.calculateTime=1e3,e.outcomeDepth=14;var r,t,i=15,a=[6,11,2,2,3],n=[{s:0,a:1,b:8,c:9,dr:[1,8]},{s:7,a:6,b:15,c:14,dr:[-1,8]},{s:56,a:57,b:48,c:49,dr:[1,-8]},{s:63,a:62,b:55,c:54,dr:[-1,-8]}];e.history=[[],[]];for(var s=0;s<2;s++)for(var o=0;o<=60;o++)e.history[s][o]=[0,63,7,56,37,26,20,43,19,29,34,44,21,42,45,18,2,61,23,40,5,58,47,16,10,53,22,41,13,46,17,50,51,52,12,11,30,38,25,33,4,3,59,60,39,31,24,32,1,62,15,48,8,55,6,57,9,54,14,49];var c=new Transposition;function f(e){return e>0?1:e<0?-1:0}function u(e){var t=e.black-e.white;return r>=i?1e4*f(t)*e.side:1e4*(t+e.space*f(t))*e.side}function d(e,r,t){var i=-1/0,a=1/0;do{var n=t==i?t+1:t;(t=v(e,r,n-1,n))<n?a=t:i=t}while(i<a);return t<n&&(t=v(e,r,t-1,t)),t}function v(r,i,s,o){if((new Date).getTime()>t)throw new Error("time out");var f=c.get(r.key,i,s,o);if(!1!==f)return f;if(0==r.space)return u(r);if(othe.findLocation(r),0==r.nextNum)return 0==r.prevNum?u(r):(othe.pass(r),-v(r,i,-o,-s));if(i<=0){var d=function(e){for(var r,t=0,i=0,s={},o=0,c=n.length;r=n[o],o<c;o++)if(0!=e[r.s]){t+=15*e[r.s],i+=e[r.s];for(var f=0;f<2;f++)if(!s[r.s+r.dr[f]]){for(var u=!0,d=0,v=1;v<=6;v++){var l=e[r.s+r.dr[f]*v];if(0==l)break;u&&l==e[r.s]?i+=l:(u=!1,d+=l)}7==v&&0!=e[r.s+7*r.dr[f]]&&(i+=d,s[r.s+6*r.dr[f]]=!0)}}else t+=-3*e[r.a],t+=-3*e[r.b],t+=-6*e[r.c];var h=0;for(o=9;o<=54;o+=6==(7&o)?3:1)if(0!=e[o])for(v=0;v<8;v++)if(0==e[othe.dire(o,v)]){h-=e[o];break}var p=(e.nextNum-e.prevNum)*e.side,m=e.space<18?e.space%2==0?-e.side:e.side:0;return(t*a[0]+i*a[1]+h*a[2]+p*a[3]+m*a[4])*e.side}(r);return c.set(r.key,d,i,0,null),d}var p=c.getBest(r.key);null!==p&&l(r.nextIndex,p);for(var m=e.history[1==r.side?0:1][r.space],g=1,k=-1/0,w=null,y=0;y<r.nextNum;y++){var b=r.nextIndex[y],x=-v(othe.newMap(r,b),i-1,-o,-s);if(x>k&&(k=x,w=b,x>s&&(s=x,g=0,h(m,b)),x>=o)){g=2;break}}return l(m,w),c.set(r.key,k,i,g,w),k}function l(e,r){if(e[0]!=r){var t=e.indexOf(r);e.splice(t,1),e.unshift(r)}}function h(e,r){if(e[0]!=r){var t=e.indexOf(r);e[t]=e[t-1],e[t-1]=r}}e.startSearch=function(a){var n=0;if(a.space<=e.outcomeDepth)return t=(new Date).getTime()+6e5,n=(r=a.space)>=i?v(a,r,-1/0,1/0):d(a,r,n),console.log("终局搜索结果：",r,a.space,a.side,n*a.side),c.getBest(a.key);t=(new Date).getTime()+e.calculateTime,r=0;try{for(;r<a.space;){n=d(a,++r,n);var s=c.getBest(a.key);console.log(r,n*a.side,s)}}catch(e){if("time out"!=e.message)throw e}return console.log("搜索结果：",r-1,a.space,a.side,n*a.side),s}}function Transposition(){var e=new Array(524288);this.set=function(t,r,n,a,s){var i=524287&t[0],u=e[i];if(u){if(u.key==t[1]&&u.depth>n)return}else u=e[i]={};u.key=t[1],u.eva=r,u.depth=n,u.flags=a,u.best=s},this.get=function(t,r,n,a){var s=e[524287&t[0]];if(!s||s.key!=t[1]||s.depth<r)return!1;switch(s.flags){case 0:return s.eva;case 1:return s.eva<=n&&s.eva;case 2:return s.eva>=a&&s.eva}},this.getBest=function(t){var r=e[524287&t[0]];return r&&r.key==t[1]?r.best:null}}function Zobrist(){for(var n=[o(),o()],t=[[],[],[]],i=0;i<64;i++)t[0][i]=[o(),o()],t[1][i]=[o(),o()],t[2][i]=[t[0][i][0]^t[1][i][0],t[0][i][1]^t[1][i][1]];function o(){return 4294967296*Math.random()>>0}this.swap=function(t){t[0]^=n[0],t[1]^=n[1]},this.set=function(n,i,o){n[0]^=t[i][o][0],n[1]^=t[i][o][1]}}function Othello(){var e=this,n=[],t=[],i=new Zobrist;e.aiSide=0;var o,r,a,s=!1,c=document.getElementById("airuning"),u=document.getElementById("pass");function d(){var t=e.aiSide==n.side||2==e.aiSide;e.findLocation(n),x(!1),p(!1),board.update(n,t),0==n.space||0==n.nextNum&&0==n.prevNum?o=setTimeout(f,450):0!=n.nextNum?t&&(s=!0,o=setTimeout(function(){x(!0),o=setTimeout(l,50)},400)):o=setTimeout(function(){e.pass(n),d(),p(!0)},450)}function l(){1==n.nextNum?e.go(n.nextIndex[0]):n.space<=58?e.go(ai.startSearch(n)):e.go(n.nextIndex[Math.random()*n.nextIndex.length>>0])}function f(){x(!1),p(!1);var e=document.getElementById("winner");e.style.display="block",e.innerHTML="游戏结束，"+(n.black==n.white?"平局!!!":n.black>n.white?"黑棋胜利!!!":"白棋胜利!!!")}function x(e){c.style.display=e?"block":"none"}function p(e){u.style.display=e?"block":"none",e&&(u.innerHTML=1==n.side?"白方无棋可下，黑方继续下子":"黑方无棋可下，白方继续下子")}e.play=function(){if(!s){clearTimeout(o),console.clear(),n=[];for(var e=0;e<64;e++)n[e]=0;n[28]=n[35]=1,n[27]=n[36]=-1,n.black=n.white=2,n.space=60,n.frontier=[];var i=[18,19,20,21,26,29,34,37,42,43,44,45];for(e=0;e<12;e++)n.frontier[i[e]]=!0;n.side=1,n.newPos=-1,n.newRev=[],n.nextIndex=[],n.next={},n.nextNum=0,n.prevNum=0,n.key=[0,0],t=[],d()}},e.dire=(r=[-8,-7,1,9,8,7,-1,-9],a=[8,0,0,0,8,7,7,7],function(e,n){return 0!=(64&(e+=r[n]))||(7&e)==a[n]?64:e}),e.findLocation=function(n){function t(t,i){for(var o=0;64!=(t=e.dire(t,i))&&n[t]==-n.side;)a[s++]=t,o++;64!=t&&n[t]==n.side||(s-=o)}n.nextIndex=[],n.next=[];for(var i=ai.history[1==n.side?0:1][n.space],o=0;o<60;o++){var r=i[o];if(n.frontier[r]){for(var a=[],s=0,c=0;c<8;c++)t(r,c);s>0&&(s!=a.length&&(a=a.slice(0,s)),n.next[r]=a,n.nextIndex.push(r))}}n.nextNum=n.nextIndex.length},e.pass=function(e){e.side=-e.side,e.prevNum=e.nextNum,i.swap(e.key)},e.newMap=function(n,t){var o=n.slice(0);o[t]=n.side,o.key=n.key.slice(0),i.set(o.key,1==n.side?0:1,t),o.frontier=n.frontier.slice(0),o.frontier[t]=!1;for(var r=0;r<8;r++){var a=e.dire(t,r);64!=a&&0==o[a]&&(o.frontier[a]=!0)}var s=n.next[t],c=s.length;for(r=0;r<c;r++)o[s[r]]=n.side,i.set(o.key,2,s[r]);return 1==n.side?(o.black=n.black+c+1,o.white=n.white-c):(o.white=n.white+c+1,o.black=n.black-c),o.space=64-o.black-o.white,o.side=-n.side,o.prevNum=n.nextNum,i.swap(o.key),o},e.goChess=function(i){t.push(n),e.go(i)},e.go=function(t){s=!1;var i=n.next[t];(n=e.newMap(n,t)).newRev=i,n.newPos=t,d()},e.historyBack=function(){s||0==t.length||(clearTimeout(o),n=t.pop(),d())}}var board=new Chessboard();var ai=new AI();var othe=new Othello();board.create();board.toDown=othe.goChess;document.getElementById("play").onclick=function(){document.getElementById("winner").style.display="none";othe.aiSide=-1;ai.calculateTime=500;ai.outcomeDepth=13;othe.play()};document.getElementById("back").onclick=function(){document.getElementById("winner").style.display="none";othe.historyBack()};</script></body></html>'''
        html3 = '''<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,minimum-scale=1.0,user-scalable=0"><title>2048</title><style> html, body, div, span, applet, object, iframe, h1, h2, h3, h4, h5, h6, p, blockquote, pre, a, abbr, acronym, address, big, cite, code, del, dfn, em, img, ins, kbd, q, s, samp, small, strike, strong, sub, sup, tt, var, b, u, i, center, dl, dt, dd, ol, ul, li, fieldset, form, label, legend, table, caption, tbody, tfoot, thead, tr, th, td, article, aside, canvas, details, embed, figure, figcaption, footer, header, hgroup, menu, nav, output, ruby, section, summary, time, mark, audio, video {margin: 0;padding: 0;border: 0;font-size: 100%;font: inherit;vertical-align: baseline }article, aside, details, figcaption, figure, footer, header, hgroup, menu, nav, section {display: block }body {line-height: 1 }ol, ul {list-style: none }blockquote, q {quotes: none }blockquote:before, blockquote:after, q:before, q:after {content: '';content: none }table {border-collapse: collapse;border-spacing: 0 }@charset "UTF-8";* {box-sizing: border-box;}a {color: #1B9AAA;text-decoration: none;border-bottom: 1px solid currentColor;}a:hover {color: #14727e;}a:focus, a:active {color: #0d4a52;}body, html {position: relative;width: 100%;height: 100%;display: -webkit-box;display: -ms-flexbox;display: flex;-webkit-box-orient: vertical;-webkit-box-direction: normal;-ms-flex-direction: column;flex-direction: column;font-family: "Arvo", Helvetica, sans-serif;font-family: 12px;color: #555;background: #F8FFE5;}strong {font-weight: bold;}p {line-height: 1.6;font-size: 16px;}@media screen and (max-width:400px) {.haiyong{font-size: 12px;}}.inspired {margin-top: 1em;font-size: 0.9rem;color: #9a9a95;}header {color: #F8FFE5;text-align: center;}header span {display: inline-block;box-sizing: border-box;width: 4rem;height: 4rem;line-height: 4rem;margin: 0 0.4rem;background: #FFC43D;}@media screen and (max-width:440px) {header span {width: 3rem;height: 3rem;line-height: 3rem;}}@media screen and (max-width:375px) {header span {width: 2.5rem;height: 2.5rem;line-height: 2.5rem;}}header span:nth-of-type(2) {background: #EF476F;}header span:nth-of-type(3) {background: #1B9AAA;}header span:nth-of-type(4) {background: #06D6A0;}h1 {font-size: 2.2rem;}.directions {padding: 2rem;border-top: 1px solid #9a9a95;border-bottom: 1px solid #9a9a95;}@media screen and (max-width:440px) {.directions{padding: 1rem;}}.container {margin: 0 auto;padding-bottom: 3.5rem;-webkit-box-flex: 1;-ms-flex: 1;flex: 1;width: 100%;max-width: 550px;text-align: center;}header .container {padding: 0;padding: 2rem 4rem;max-width: 900px;}@media screen and (max-width:440px) {header .container {padding: 1rem 2rem;}}.scores {display: -webkit-box;display: -ms-flexbox;display: flex;-webkit-box-pack: center;-ms-flex-pack: center;justify-content: center;}.score-container {display: -webkit-box;display: -ms-flexbox;display: flex;-webkit-box-pack: center;-ms-flex-pack: center;justify-content: center;-webkit-box-align: center;-ms-flex-align: center;align-items: center;margin: 0.8rem;font-size: 1.2rem;line-height: 1;color: #555;}.score-container.best-score {color: #9a9a95;}.score {margin-left: 1rem;position: relative;font-weight: bold;font-size: 1.5rem;vertical-align: middle;text-align: right;}.game {position: relative;margin: 0 auto;background: #9a9a95;padding: 7px;display: inline-block;border-radius: 3px;box-sizing: border-box;}.tile-container {border-radius: 6px;position: relative;width: 270px;height: 270px;}.tile, .background {display: block;color: #F8FFE5;position: absolute;width: 67.5px;height: 67.5px;box-sizing: border-box;text-align: center;}.background {z-index: 1;text-align: center;border: 5px solid #9a9a95;background-color: #F8FFE5;}.tile {opacity: 0;z-index: 2;background: #FFC43D;color: #F8FFE5;display: -webkit-box;display: -ms-flexbox;display: flex;-webkit-box-align: center;-ms-flex-align: center;align-items: center;-webkit-box-pack: center;-ms-flex-pack: center;justify-content: center;font-size: 1.8rem;align-items: center;-webkit-transition: 110ms ease-in-out;transition: 110ms ease-in-out;border-radius: 3px;border: 7px solid #9a9a95;box-sizing: border-box;}.tile--4 {background: #EF476F;color: #F8FFE5;}.tile--8 {background: #1B9AAA;color: #F8FFE5;}.tile--16 {background: #06D6A0;color: #F8FFE5;}.tile--32 {background: #f37694;color: #F8FFE5;}.tile--64 {background: #22c2d6;color: #F8FFE5;}.tile--128 {background: #17f8be;color: #F8FFE5;}.tile--256 {background: #ffd470;color: #F8FFE5;}.tile--512 {background: #eb184a;color: #F8FFE5;}.tile--1024 {background: #14727e;color: #F8FFE5;}.tile--2048 {background: #05a47b;color: #F8FFE5;}.tile--pop {-webkit-animation: pop 0.3s ease-in-out;animation: pop 0.3s ease-in-out;-webkit-animation-fill-mode: forwards;animation-fill-mode: forwards;}.tile--shrink {-webkit-animation: shrink 0.5s ease-in-out;animation: shrink 0.5s ease-in-out;-webkit-animation-fill-mode: forwards;animation-fill-mode: forwards;}.add {position: absolute;opacity: 0;left: 120%;top: 0;font-size: 1rem;color: #1B9AAA;}.add.active {-webkit-animation: add 0.8s ease-in-out;animation: add 0.8s ease-in-out;}@-webkit-keyframes add {0% {opacity: 1;top: 0;}100% {opacity: 0;top: -100%;}}@keyframes add {0% {opacity: 1;top: 0;}100% {opacity: 0;top: -100%;}}@-webkit-keyframes pop {0% {-webkit-transform: scale(0.5);transform: scale(0.5);opacity: 0;}90% {-webkit-transform: scale(1.1);transform: scale(1.1);opacity: 1;}100% {-webkit-transform: scale(1);transform: scale(1);opacity: 1;}}@keyframes pop {0% {-webkit-transform: scale(0.5);transform: scale(0.5);opacity: 0;}90% {-webkit-transform: scale(1.1);transform: scale(1.1);opacity: 1;}100% {-webkit-transform: scale(1);transform: scale(1);opacity: 1;}}@-webkit-keyframes shrink {0% {-webkit-transform: scale(1);transform: scale(1);opacity: 1;}100% {-webkit-transform: scale(0.9);transform: scale(0.9);opacity: 0.9;}}@keyframes shrink {0% {-webkit-transform: scale(1);transform: scale(1);opacity: 1;}100% {-webkit-transform: scale(0.9);transform: scale(0.9);opacity: 0.9;}}.end {opacity: 0;position: absolute;top: 0;left: 0;width: 100%;height: 100%;z-index: -1;display: -webkit-box;display: -ms-flexbox;display: flex;-webkit-box-orient: vertical;-webkit-box-direction: normal;-ms-flex-direction: column;flex-direction: column;-webkit-box-pack: center;-ms-flex-pack: center;justify-content: center;-webkit-box-align: center;-ms-flex-align: center;align-items: center;background: rgba(85, 85, 85, 0.9);color: white;font-size: 2rem;-webkit-transition: opacity 0.3s ease-in-out;transition: opacity 0.3s ease-in-out;}.end btn {margin-top: 1rem;}.end.active {opacity: 1;z-index: 1000;}.monkey {font-size: 3rem;margin: 1rem 0;}.btn {font-family: inherit;font-size: 1rem;border: none;background: #1B9AAA;letter-spacing: 1px;color: white;font-weight: 300;padding: 0.9em 1.5em;border-radius: 3px;border: 1px solid transparent;cursor: pointer;}.btn:hover {background-color: #14727e;}.btn:active {background-color: #0d4a52;}.btn:focus {box-shadow: 0 0 10px #0d4a52 inset;outline: none;}.not-recommended {display: -webkit-box;display: -ms-flexbox;display: flex;-webkit-box-pack: center;-ms-flex-pack: center;justify-content: center;-webkit-box-align: center;-ms-flex-align: center;align-items: center;margin-top: 0.8rem;}.not-recommended *+* {margin-left: 10px;}.not-recommended__item+.not-recommended__annotation:before {font-size: 30px;content: "😐";}.not-recommended__item:hover+.not-recommended__annotation:before {content: "😟";}.not-recommended__item:focus+.not-recommended__annotation:before {content: "😄";}.not-recommended__item:active+.not-recommended__annotation:before {content: "😨";}.page-footer {position: fixed;right: 35px;bottom: 20px;display: flex;align-items: center;padding: 5px;color: black;background: rgba(255, 255, 255, 0.65);}.page-footer a {display: flex;margin-left: 4px;}.touxiang{bottom: 0px;width:30px;height:30px;}</style></head><body><header><div class="container"><h1><span>2</span><span>0</span><span>4</span><span>8</span></h1></div></header><div class="container"><div class="scores"><div class="score-container best-score">历史最佳:<div class="score"><div id="bestScore">0</div></div></div><div class="score-container">分数:<div class="score"><div id="score">0</div><div class="add" id="add"></div></div></div></div><div class="game"><div id="tile-container" class="tile-container"></div><div class="end" id="end">游戏结束<div class="monkey">🙈</div><button class="btn not-recommended__item js-restart-btn" id="try-again">再试一次</button></div></div><div class="not-recommended"><button class="btn not-recommended__item js-restart-btn" id="restart">重新启动游戏</button><span class="not-recommended__annotation"></span></div><br><div class="directions"><p id="haiyong" class="haiyong"><strong>如何玩：</strong> 使用键盘方向键键移动数字方块。相邻的两个方块数字相同，它们可合并成一个！</p></div></div><script>"use strict";var _extends=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var r in n)Object.prototype.hasOwnProperty.call(n,r)&&(e[r]=n[r])}return e},game=null,bestScore=0,scoreDiv=document.getElementById("score"),bestScoreDiv=document.getElementById("bestScore"),addDiv=document.getElementById("add"),endDiv=document.getElementById("end"),size=4,nextId=1,score=0;function initGame(){game=Array(size*size).fill(null),initBestScore()}function initBestScore(){bestScore=localStorage.getItem("bestScore")||0,bestScoreDiv.innerHTML=bestScore}function updateDOM(e,t){var n=getNewElementsDOM(e,t),r=getExistingElementsDOM(e,t);removeElements(getMergedTiles(t)),drawGame(n,!0),drawGame(r)}function removeElements(e){var t=e,n=Array.isArray(t),r=0;for(t=n?t:t[Symbol.iterator]();;){var i;if(n){if(r>=t.length)break;i=t[r++]}else{if((r=t.next()).done)break;i=r.value}var a=i,o=function(){if(c){if(d>=s.length)return"break";u=s[d++]}else{if((d=s.next()).done)return"break";u=d.value}var e=u,t=document.getElementById(e);positionTile(a,t),t.classList.add("tile--shrink"),setTimeout(function(){t.remove()},100)},s=a.mergedIds,c=Array.isArray(s),d=0;for(s=c?s:s[Symbol.iterator]();;){var u;if("break"===o())break}}}function getMergedTiles(e){return e.filter(function(e){return e&&e.mergedIds})}function getNewElementsDOM(e,t){var n=e.filter(function(e){return e}).map(function(e){return e.id});return t.filter(function(e){return e&&-1===n.indexOf(e.id)})}function getExistingElementsDOM(e,t){var n=e.filter(function(e){return e}).map(function(e){return e.id});return t.filter(function(e){return e&&-1!==n.indexOf(e.id)})}function drawBackground(){var e=document.getElementById("tile-container");e.innerHTML="";for(var t=0;t<game.length;t++){game[t];var n=document.createElement("div"),r=t%size,i=Math.floor(t/size);n.style.top=67.5*i+"px",n.style.left=67.5*r+"px",n.classList.add("background"),e.appendChild(n)}}function positionTile(e,t){var n=e.index%size,r=Math.floor(e.index/size);t.style.top=67.5*r+"px",t.style.left=67.5*n+"px"}function drawGame(e,t){for(var n=document.getElementById("tile-container"),r=0;r<e.length;r++){var i=e[r];if(i)if(t)!function(){var e=document.createElement("div");positionTile(i,e),e.classList.add("tile","tile--"+i.value),e.id=i.id,setTimeout(function(){e.classList.add("tile--pop")},i.mergedIds?1:150),e.innerHTML="<p>"+i.value+"</p>",n.appendChild(e)}();else{var a=document.getElementById(i.id);positionTile(i,a)}}}function gameOver(){if(0===game.filter(function(e){return null===e}).length)return!game.find(function(e,t){var n=!(!game[t+1]||(t+1)%4==0)&&e.value===game[t+1].value,r=!!game[t+4]&&e.value===game[t+4].value;return!(!n&&!r)})}function generateNewNumber(){return 100*Math.random()<=90?2:4}function addRandomNumber(){var e=game.map(function(e,t){return t}).filter(function(e){return null===game[e]});if(0!==e.length){var t=e[Math.floor(Math.random()*e.length)],n={id:nextId++,index:t,value:generateNewNumber()};game.splice(t,1,n)}}function getIndexForPoint(e,t){return t*size+e}function reflectGrid(e){for(var t=Array(size*size).fill(0),n=0;n<size;n++)for(var r=0;r<size;r++){var i=getIndexForPoint(r,n),a=getIndexForPoint(size-r-1,n);t[i]=e[a]}return t}function rotateLeft90Deg(e){for(var t=Array(size*size).fill(0),n=0;n<size;n++)for(var r=0;r<size;r++){var i=getIndexForPoint(r,n),a=getIndexForPoint(size-1-n,r);t[i]=e[a]}return t}function rotateRight90Deg(e){for(var t=Array(size*size).fill(0),n=0;n<size;n++)for(var r=0;r<size;r++){var i=getIndexForPoint(r,n),a=getIndexForPoint(n,size-1-r);t[i]=e[a]}return t}function shiftGameRight(e){var t=reflectGrid(e);return reflectGrid(t=shiftGameLeft(t))}function shiftGameLeft(e){for(var t=[],n=0,r=0;r<size;r++){var i=4*r,a=size+4*r,o=e.slice(i,a).filter(function(e){return e}),s=o,c=Array.isArray(s),d=0;for(s=c?s:s[Symbol.iterator]();;){var u;if(c){if(d>=s.length)break;u=s[d++]}else{if((d=s.next()).done)break;u=d.value}delete u.mergedIds}for(var l=0;l<o.length-1;l++)if(o[l].value===o[l+1].value){var m=2*o[l].value;o[l]={id:nextId++,mergedIds:[o[l].id,o[l+1].id],value:m},o.splice(l+1,1),score+=m,n+=m}for(;o.length<size;)o.push(null);t=[].concat(t,o)}return n>0&&(scoreDiv.innerHTML=score,addDiv.innerHTML="+"+n,addDiv.classList.add("active"),setTimeout(function(){addDiv.classList.remove("active")},800),score>bestScore&&(localStorage.setItem("bestScore",score),initBestScore())),t}function shiftGameUp(e){var t=rotateLeft90Deg(e);return rotateRight90Deg(t=shiftGameLeft(t))}function shiftGameDown(e){var t=rotateRight90Deg(e);return rotateLeft90Deg(t=shiftGameLeft(t))}for(var buttons=document.querySelectorAll(".js-restart-btn"),length=buttons.length,i=0;i<length;i++)document.addEventListener?buttons[i].addEventListener("click",function(){newGameStart()}):buttons[i].attachEvent("onclick",function(){newGameStart()});document.addEventListener("keydown",handleKeypress),document.addEventListener("touchstart",handleTouchStart,!1),document.addEventListener("touchmove",handleTouchMove,!1);var xDown=null,yDown=null;function handleTouchStart(e){xDown=e.touches[0].clientX,yDown=e.touches[0].clientY}function handleTouchMove(e){var t=[].concat(game);if(xDown&&yDown){var n=e.touches[0].clientX,r=e.touches[0].clientY,i=xDown-n,a=yDown-r;game=(game=Math.abs(i)>Math.abs(a)?i>0?shiftGameLeft(game):shiftGameRight(game):a>0?shiftGameUp(game):shiftGameDown(game)).map(function(e,t){return e?_extends({},e,{index:t}):null}),addRandomNumber(),updateDOM(t,game),gameOver()?setTimeout(function(){endDiv.classList.add("active")},800):(xDown=null,yDown=null)}}function handleKeypress(e){const t=[37,38,39,40];var n=event.altKey||event.ctrlKey||event.metaKey||event.shiftKey,r=event.which;console.log(r);var i=[].concat(game);if(!n){switch(event.preventDefault(),r){case 37:game=shiftGameLeft(game);break;case 38:game=shiftGameUp(game);break;case 39:game=shiftGameRight(game);break;case 40:game=shiftGameDown(game)}if(game=game.map(function(e,t){return e?_extends({},e,{index:t}):null}),t.includes(r)&&addRandomNumber(),updateDOM(i,game),gameOver())return void setTimeout(function(){endDiv.classList.add("active")},800)}}function newGameStart(){document.getElementById("tile-container").innerHTML="",endDiv.classList.remove("active"),score=0,scoreDiv.innerHTML=score,initGame(),drawBackground();var e=[].concat(game);addRandomNumber(),addRandomNumber(),updateDOM(e,game)}newGameStart();</script></body></html>'''
        html4 = '''<!doctype html><html><head><meta charset="UTF-8" /><title>Off The Line</title></head><body><center><div id="game"></div></center><script type="text/javascript">'use strict';var aa="function"==typeof Object.create?Object.create:function(a){function b(){}b.prototype=a;return new b},ba;if("function"==typeof Object.setPrototypeOf)ba=Object.setPrototypeOf;else{var ca;a:{var da={Za:!0},ea={};try{ea.__proto__=da;ca=ea.Za;break a}catch(a){}ca=!1}ba=ca?function(a,b){a.__proto__=b;if(a.__proto__!==b)throw new TypeError(a+" is not extensible");return a}:null}var fa=ba;function c(a,b){a.prototype=aa(b.prototype);a.prototype.constructor=a;if(fa)fa(a,b);else for(var e in b)if("prototype"!=e)if(Object.defineProperties){var g=Object.getOwnPropertyDescriptor(b,e);g&&Object.defineProperty(a,e,g)}else a[e]=b[e];a.mb=b.prototype}var ha="function"==typeof Object.defineProperties?Object.defineProperty:function(a,b,e){a!=Array.prototype&&a!=Object.prototype&&(a[b]=e.value)},d="undefined"!=typeof window&&window===this?this:"undefined"!=typeof global&&null!=global?global:this;function ia(){ia=function(){};d.Symbol||(d.Symbol=ja)}var ja=function(){var a=0;return function(b){return"jscomp_symbol_"+(b||"")+a++}}();function ka(){ia();var a=d.Symbol.iterator;a||(a=d.Symbol.iterator=d.Symbol("iterator"));"function"!=typeof Array.prototype[a]&&ha(Array.prototype,a,{configurable:!0,writable:!0,value:function(){return la(this)}});ka=function(){}}function la(a){var b=0;return ma(function(){return b<a.length?{done:!1,value:a[b++]}:{done:!0}})}function ma(a){ka();a={next:a};a[d.Symbol.iterator]=function(){return this};return a}function f(a,b){if(b){var e=d;a=a.split(".");for(var g=0;g<a.length-1;g++){var h=a[g];h in e||(e[h]={});e=e[h]}a=a[a.length-1];g=e[a];b=b(g);b!=g&&null!=b&&ha(e,a,{configurable:!0,writable:!0,value:b})}}f("Number.MAX_SAFE_INTEGER",function(){return 9007199254740991});f("String.prototype.endsWith",function(a){return a?a:function(a,e){if(null==this)throw new TypeError("The 'this' value for String.prototype.endsWith must not be null or undefined");if(a instanceof RegExp)throw new TypeError("First argument to String.prototype.endsWith must not be a regular expression");var b=this+"";a+="";void 0===e&&(e=b.length);e=Math.max(0,Math.min(e|0,b.length));for(var h=a.length;0<h&&0<e;)if(b[--e]!=a[--h])return!1;return 0>=h}});function na(a,b){ka();a instanceof String&&(a+="");var e=0,g={next:function(){if(e<a.length){var h=e++;return{value:b(h,a[h]),done:!1}}g.next=function(){return{done:!0,value:void 0}};return g.next()}};g[Symbol.iterator]=function(){return g};return g}f("Array.prototype.keys",function(a){return a?a:function(){return na(this,function(a){return a})}});f("Object.values",function(a){return a?a:function(a){var b=[],g;for(g in a)Object.prototype.hasOwnProperty.call(a,g)&&b.push(a[g]);return b}});function oa(a,b,e,g,h,m,r,t){var n={V:!1},y=(a-r)*(g-t)-(b-t)*(e-r),G=(a-h)*(g-m)-(b-m)*(e-h);0>y*G&&(h=(h-a)*(t-b)-(m-b)*(r-a),y=h+G-y,0>h*y&&(n.time=h/(h-y),n.x=a+n.time*(e-a),n.y=b+n.time*(g-b),n.V=!0));return n}function k(a,b){return a.x*b.x+a.y*b.y}function pa(){if(void 0===window||void 0===window.localStorage)return 0;var a=window.localStorage.getItem("best_"+l);return null!==a?parseInt(a,10):0}function qa(){var a="简单模式";1===l?a="困难模式":2===l&&(a="专家模式");return a}function ra(){p.B.setTransform(1,0,0,1,0,0)}function sa(){p.B.setTransform(1,0,0,1,0,0);p.B.translate(.5*q,.5*u);p.B.translate(-v+v*Math.random()*2,-v+v*Math.random()*2);p.B.scale(w,-w)}var v=0,ta=0,x=0,ua=0;function va(a){0<x&&(x-=a,v=Math.max(x/ua*ta,0))}var w=1,A=0;function B(a){0<A&&(A-=a,a=A/.2,w=Math.max(1+a*a*a*.15,1))}var C=[];function wa(a){C.forEach(function(b,e){var g=b.ma/.5,h=1-g*g*g,m=b.x+Math.cos(b.Na)*b.Ja*h,r=b.y+Math.sin(b.Na)*b.Ja*h;h=b.angle+1*Math.PI*h;0==e%2&&(h=-h);p.B.globalAlpha=.25>g?g/.25:1;p.B.save();p.B.translate(m,r);p.B.rotate(h);e=p.B.lineWidth;p.B.lineWidth=4;p.B.strokeStyle="#08F";p.B.shadowColor="#08F";p.B.beginPath();p.B.moveTo(-6,0);p.B.lineTo(6,0);p.B.stroke();p.B.restore();p.B.lineWidth=e;p.B.globalAlpha=1;b.ma-=a;0>=b.ma&&(b.S=!0)});C=C.filter(function(a){return!0!==a.S})}function xa(a,b){for(var e=0;10>e;e++)C.push({x:a,y:b,ma:.5,S:!1,angle:Math.random()*Math.PI*2,Na:360*Math.random()*Math.PI/180,Ja:15+40*Math.random()})}function D(){this.oa=this.na=this.ea=this.da=this.y=this.x=0;this.H=12;this.speed=0===l?250:400;this.hb=.2;this.$=Number.MAX_SAFE_INTEGER;this.T=this.K=0;this.Z=this.Sa;this.sa={x:0,y:0};this.Ia=1500;this.R=!1;this.angle=0;this.Y=180;this.Xa=this.Ua=0;var a=ya(this.T,this.K);this.x=a.x;this.y=a.y;this.na=this.x;this.oa=this.y;this.da=this.x;this.ea=this.y;this.Ta=this.x;this.Wa=this.y}D.prototype.update=function(a){this.na=this.da;this.oa=this.ea;this.da=this.x;this.ea=this.y;this.angle+=this.Y*a;void 0!==this.Z&&this.Z(a)};D.prototype.Sa=function(a){var b=this;this.K+=this.speed*a;0>this.K&&(this.K+=E.O[this.T]);this.K%=E.O[this.T];var e=ya(this.T,this.K);this.x=e.x;this.y=e.y;this.Ua=e.ya;this.Xa=e.Ca;p.entities.forEach(function(a){a instanceof F&&(a=oa(b.na,b.oa,b.x,b.y,a.va,a.za,a.wa,a.Aa),a.V&&(xa(a.x,a.y),b.U()))});if(!this.R){this.$+=a;if(p.M||p.W.space)this.$=0;this.$<=this.hb&&(this.sa={x:e.Pa*this.Ia,y:e.Qa*this.Ia},this.Ta=this.x,this.Wa=this.y,this.Z=this.fb,H("a",5,.01),H("a#",5,.01,.01),H("b",5,.01,.02))}};D.prototype.fb=function(a){var b=this;this.x+=this.sa.x*a;this.y+=this.sa.y*a;p.entities.forEach(function(a){a instanceof F&&(a=oa(b.na,b.oa,b.x,b.y,a.va,a.za,a.wa,a.Aa),a.V&&(xa(a.x,a.y),b.U()))});(this.x<.5*-q-this.H||this.x>.5*q+this.H||this.y<.5*-u-this.H||this.y>.5*u+this.H)&&this.U();if(!this.R&&(p.entities.forEach(function(a){if(a instanceof I){var e=b.da,g=b.ea,h=b.x,n=b.y,y=a.x,G=a.y;var z={x:h-e,y:n-g};e={x:y-e,y:G-g};h={x:y-h,y:G-n};n=k(e,z);0>=n?z=k(e,e):(z=k(z,z),z=n>=z?k(h,h):k(e,e)-n*n/z);z<=a.cb&&a.U()}}),a=za(this.da,this.ea,this.x,this.y),a.V)){var e=a.x-this.Ta,g=a.y-this.Wa;5<e*e+g*g&&(this.K=a.ab,this.T=a.group,a=ya(this.T,this.K),this.x=a.x,this.y=a.y,this.$=Number.MAX_SAFE_INTEGER,this.Z=this.Sa,0>a.ya*this.Ua+a.Ca*this.Xa&&(this.speed=-this.speed),v=ta=2.5,x=ua=.15,H("a",4,.01),H("a#",4,.01,.01))}};D.prototype.$a=function(){};D.prototype.ca=function(){if(!this.R){p.B.save();p.B.translate(this.x,this.y);p.B.rotate(this.angle);var a=p.B.lineWidth;p.B.lineWidth=4;p.B.strokeStyle="#08F";p.B.shadowColor="#08F";p.B.beginPath();p.B.rect(.5*-this.H,.5*-this.H,this.H,this.H);p.B.stroke();p.B.restore();p.B.lineWidth=a}};D.prototype.U=function(){J=Math.max(J-1,0);this.R=!0;this.Z=this.$a;v=ta=5;x=ua=.2;H("a",1,.2,0,"square");var a=p;if(a.ka&&a.G){var b=a.G.createBufferSource();b.buffer=a.Oa;b.loop=!0;b.start(a.G.currentTime+0);b.stop(a.G.currentTime+0+.05);b.connect(a.G.destination)}};function I(a,b,e,g,h){this.xa=a;this.Ba=b;this.x=a;this.y=b;this.H=8;this.Ha=20;this.cb=this.Ha*this.Ha;this.angle=0;this.Y=180;this.active=!0;this.offset=void 0!==e?e:0;this.ja=void 0!==g?g*Math.PI/180:0;this.Ra=void 0!==h?h*Math.PI/180:0;this.fa=0;this.Ea=.5}I.prototype.update=function(a){this.angle-=this.Y*a;if(0!==this.offset){var b=Math.sin(this.ja);this.x=this.xa+Math.cos(this.ja)*this.offset;this.y=this.Ba+b*this.offset;0!==this.Ra&&(this.ja+=this.Ra*a)}this.active||(this.fa+=a)};I.prototype.ca=function(){if(this.active||this.fa<this.Ea){var a=p.B.globalAlpha,b=1;if(!this.active){var e=1-this.fa/this.Ea;e*=e*e*e*e;b+=3*(1-e);p.B.globalAlpha=e}p.B.save();p.B.translate(this.x,this.y);p.B.rotate(this.angle*Math.PI/180);p.B.scale(b,b);p.B.lineWidth=2;p.B.strokeStyle="#FF0";p.B.shadowColor="#FF0";p.B.beginPath();p.B.rect(.5*-this.H,.5*-this.H,this.H,this.H);p.B.stroke();p.B.restore();p.B.globalAlpha=a}};I.prototype.U=function(){this.active&&(this.active=!1,H("g",7,.025))};function F(a,b,e,g,h,m,r,t,n){this.xa=a;this.Ba=b;this.length=e;this.ga=.5*e;this.angle=void 0!==g?g*Math.PI/180:0;this.Y=void 0!==h?h*Math.PI/180:0;this.Va=void 0!==m?m:0;this.Ya=void 0!==r?r:0;this.ba=void 0!==t?t:0;this.eb=void 0!==n?n:0;this.P=this.ba;this.ia=this.ha=!0;this.pa=0;Aa(this)}F.prototype.update=function(a){var b=!1;0!==this.Y&&(this.angle+=this.Y*a,b=!0);0===this.Va&&0===this.Ya||0===this.ba||(this.pa=this.ha?this.ia?1-this.P/this.ba:this.P/this.ba:this.ia?0:1,this.P-=a,0>=this.P&&(this.ha?(this.P=this.eb,this.ia=!this.ia):this.P=this.ba,this.ha=!this.ha),b=!0);b&&Aa(this)};function Aa(a){var b=Math.cos(a.angle),e=Math.sin(a.angle),g=a.xa+a.Va*a.pa,h=a.Ba+a.Ya*a.pa;a.va=g-b*a.ga;a.za=h-e*a.ga;a.wa=g+b*a.ga;a.Aa=h+e*a.ga}F.prototype.ca=function(){p.B.save();p.B.lineWidth=2;p.B.strokeStyle="#F00";p.B.shadowColor="#F00";p.B.beginPath();p.B.moveTo(this.va,this.za);p.B.lineTo(this.wa,this.Aa);p.B.stroke();p.B.restore()};function Ba(a){wa(a);ra();2==l&&(a=u-30,p.B.fillStyle="#FFF",p.B.fillRect(10,a,E.N/E.L*(q-20),20));p.B.shadowColor="#FFF";K({text:"关卡 "+(L+1)+" - "+(E?E.name:""),x:10,y:30,fontSize:24,fontStyle:"bold"});K({text:"BEST: "+(pa()+1),x:10,y:50,fontSize:15,fontStyle:"bold",color:"#FFF"});if(2===l)p.B.shadowColor="#08F",K({text:"无限生命",x:630,y:25,fontSize:15,fontStyle:"bold",color:"#08F",textAlign:"right"}),K({text:"PRESS [ESC] TO QUIT",x:630,y:45,fontSize:15,fontStyle:"bold",color:"#08F",textAlign:"right"});else{a=0===l?10:5;for(var b=0===l?440:536,e=0;e<a;e++)e<J?(p.B.lineWidth=3,p.B.strokeStyle="#08F",p.B.shadowColor="#08F",p.B.save(),p.B.translate(b+4+20*e,18),p.B.beginPath(),p.B.rect(-5,-5,10,10),p.B.stroke(),p.B.restore()):(p.B.shadowColor="#F00",K({text:"x",x:b+19.6*e,y:30,fontSize:24,fontStyle:"bold",color:"#F00"}))}p.state===Ca&&(19===L?(p.B.shadowColor="#555",p.B.fillStyle="#555",p.B.fillRect(0,100,q,110),a=250>Date.now()%500?"#08F":"#FF0",p.B.shadowColor=a,K({text:"恭喜!",x:.5*q,y:150,fontSize:40,fontStyle:"bold",color:a,textAlign:"center"}),p.B.shadowColor="#FFF",K({text:qa()+" 通关",x:.5*q,y:180,fontSize:20,fontStyle:"bold",color:"#FFF",textAlign:"center"}),K({text:"点击返回主菜单",x:.5*q,y:200,fontSize:14,fontStyle:"bold",color:"#FFF",textAlign:"center"})):(p.B.shadowColor="#333",p.B.fillStyle="#333",p.B.fillRect(0,52,q,140),p.B.shadowColor="#F00",K({text:"GAME OVER",x:.5*q,y:100,fontSize:40,fontStyle:"bold",color:"#F00",textAlign:"center"}),p.B.shadowColor="#FFF",K({text:qa(),x:.5*q,y:130,fontSize:20,fontStyle:"bold",color:"#FFF",textAlign:"center"}),K({text:"SCORE: "+(L+1),x:.5*q,y:155,fontSize:20,fontStyle:"bold",color:"#FFF",textAlign:"center"}),K({text:"BEST: "+(pa()+1),x:.5*q,y:180,fontSize:20,fontStyle:"bold",color:"#FFF",textAlign:"center"})))}var M=[{text:"简单模式",width:255,ra:"(慢速 + 10 生命)"},{text:"困难模式",width:255,ra:"(快速 + 5 生命)"},{text:"专家模式",width:255,ra:"(快速 + 限时)"}],Da=-1;function N(a){O(a);p.B.save();ra();p.B.shadowColor="#08F";K({text:"纵横无界",x:15,y:10,fontSize:70,fontStyle:"bold italic",color:"#08F",textAlign:"left",textBaseline:"top"});p.B.shadowColor="#08F";K({text:" off the line ",x:25,y:85,fontSize:20,fontStyle:"bold italic",color:"#08F",textAlign:"left",textBaseline:"top"});a=-1;for(var b=0;b<M.length;b++){var e=p.aa.y>=350+40*b&&p.aa.y<350+40*(b+1)&&0<=p.aa.x&&p.aa.x<M[b].width,g=e?"#FF0":"#FFF";p.B.shadowColor=g;K({text:M[b].text,x:15,y:350+40*b,fontSize:35,fontStyle:"bold italic",color:g,textAlign:"left",textBaseline:"top"});e&&(a=b,p.B.shadowColor="#888",K({text:M[b].ra,x:-15+M[b].width,y:40*b+362,fontSize:12,fontStyle:"bold italic",color:"#888",textAlign:"left",textBaseline:"top"}))}p.B.restore();a!==Da&&(-1!==a&&H("a",5,.025),Da=a);-1!==a&&p.M&&(l=a,J=0===l?10:5,L=0,Ea(),p.M=!1,p.B.shadowBlur=0,p.state=Fa,p.la=Ba)}function Fa(a){p.B.shadowBlur=10;O(a);p.W.escape&&2===l&&(p.entities=[],p.M=!1,p.B.shadowBlur=20,p.state=N,p.la=void 0,H("a",4,.05,0),H("b",4,.05,.05));if(P.R||Ga())if(Ha-=a,0>=Ha)if(Ga()&&19===L){p.state=Ca;for(var b=0;3>b;b++)H("d",5,.05,.3*b),H("e",5,.05,.3*b+.05),H("g",5,.05,.3*b+.1),H("a",5,.05,.3*b+.15),H("b",5,.05,.3*b+.2),H("d",5,.05,.3*b+.25);H("c",6,.5,.9)}else 0===J&&2!==l?(p.state=Ca,H("a#",4,.05,0),H("g",4,.05,.05),H("e",4,.05,.1),H("d",4,.15,.15)):(P.R||(L=(L+1)%20),Ea());va(a);B(a);sa()}function Ea(){var a=L;p.entities=[];w=1.15;A=.2;B(0);va(0);B(0);sa();0==a?E=new Q:1==a?E=new R:2==a?E=new S:3==a?E=new T:4==a?E=new U:5==a?E=new V:6==a?E=new W:7==a?E=new X:8==a?E=new Ia:9==a?E=new Ja:10==a?E=new Ka:11==a?E=new La:12==a?E=new Ma:13==a?E=new Na:14==a?E=new Oa:15==a?E=new Pa:16==a?E=new Qa:17==a?E=new Ra:18==a?E=new Sa:19==a&&(E=new Ta);Y(E);P=new D;Y(P);Ha=1;void 0!==window&&void 0!==window.localStorage&&window.localStorage.setItem("best_"+l,Math.max(L.toString(),pa()));H("d",4,.05,0);H("e",4,.05,.05);H("g",4,.05,.1);H("a#",4,.15,.15)}function Ca(a){O(a);p.M&&(p.entities=[],p.M=!1,p.B.shadowBlur=20,p.state=N,p.la=void 0,H("a",4,.05,0),H("b",4,.05,.05));va(a);B(a);sa()}var Ua=[],Va=400,Wa=4E3,Xa=2;function O(a){p.W.s&&(p.ka=!p.ka);p.B.save();ra();for(var b=0;b<Xa;b++)Ua.push({x:q,y:Math.random()*u,S:!1});p.B.lineWidth=2;p.B.strokeStyle=p.state===N||p.state===Ya?"#111":"#090909";b=p.B.shadowBlur;p.B.shadowBlur=0;Ua.forEach(function(b){b.x-=Wa*a;b.x<-Va&&(b.S=!0);p.B.beginPath();p.B.moveTo(b.x,b.y);p.B.lineTo(b.x+Va,b.y);p.B.stroke()});Ua=Ua.filter(function(a){return!0!==a.S});p.B.restore();p.B.shadowBlur=b}function Z(){this.A=[];this.J=[];this.O=[];this.C=[];this.N=this.L=7;this.F();for(var a=0;a<this.A.length;a++){this.O.push(0);this.J.push([]);for(var b=0;b<this.A[a].length-1;b++){var e=this.A[a][b+1].x-this.A[a][b].x,g=this.A[a][b+1].y-this.A[a][b].y;e=Math.sqrt(e*e+g*g);this.O[a]+=e;this.J[a].push(e)}b=this.A[a][0].x-this.A[a][this.A[a].length-1].x;e=this.A[a][0].y-this.A[a][this.A[a].length-1].y;b=Math.sqrt(b*b+e*e);this.O[a]+=b;this.J[a].push(b)}this.D()}Z.prototype.F=function(){};Z.prototype.D=function(){};Z.prototype.update=function(a){2!=l||Ga()||P.R||(this.N=Math.max(this.N-a,0),0>=this.N&&(xa(P.x,P.y),P.U()))};Z.prototype.ca=function(){p.B.lineWidth=2;p.B.strokeStyle="#FFF";p.B.shadowColor="#FFF";for(var a=0;a<this.A.length;a++){p.B.beginPath();p.B.moveTo(this.A[a][0].x,this.A[a][0].y);for(var b=1;b<this.A[a].length;b++)p.B.lineTo(this.A[a][b].x,this.A[a][b].y);p.B.lineTo(this.A[a][0].x,this.A[a][0].y);p.B.stroke()}};function ya(a,b){var e=E;b%=e.O[a];for(var g=0,h=0;h<e.J[a].length;h++){var m=g+e.J[a][h];if(b>=g&&b<m){var r=(b-g)/e.J[a][h];g=h;m=(h+1)%e.A[a].length;var t=e.A[a][m].x-e.A[a][g].x,n=e.A[a][m].y-e.A[a][g].y;b=e.A[a][g].x+t*r;r=e.A[a][g].y+n*r;if(void 0!==e.C[a]&&void 0!==e.C[a][h])return{x:b,y:r,Pa:e.C[a][h].x,Qa:e.C[a][h].y,ya:t,Ca:n};t=(e.A[a][m].x-e.A[a][g].x)/e.J[a][h];a=(e.A[a][m].y-e.A[a][g].y)/e.J[a][h];return{x:b,y:r,Pa:a,Qa:-t,ya:t,Ca:a}}g=m}return{x:e.A[0][0].x,y:e.A[0][0].y}}function za(a,b,e,g){for(var h=E,m=0;m<h.J.length;m++)for(var r=0,t=0;t<h.J[m].length;t++){var n=t,y=(t+1)%h.A[m].length;n=oa(h.A[m][n].x,h.A[m][n].y,h.A[m][y].x,h.A[m][y].y,a,b,e,g);if(n.V)return n.ab=r+h.J[m][t]*n.time,n.group=m,n;r+=h.J[m][t]}return{V:!1}}function Ga(){var a=!0;p.entities.forEach(function(b){b instanceof I&&b.active&&(a=!1)});return a}function Q(a){Z.apply(this,arguments)}c(Q,Z);Q.prototype.F=function(){this.A.push([]);this.A[0].push({x:-100,y:100});this.A[0].push({x:100,y:100});this.A[0].push({x:100,y:-100});this.A[0].push({x:-100,y:-100});this.name="盒子"};Q.prototype.D=function(){Y(new I(0,0));Y(new I(-50,0));Y(new I(50,0));Y(new I(-25,0));Y(new I(25,0));Y(new I(0,50));Y(new I(-50,50));Y(new I(50,50));Y(new I(-25,50));Y(new I(25,50));Y(new I(0,-50));Y(new I(-50,-50));Y(new I(50,-50));Y(new I(-25,-50));Y(new I(25,-50))};function R(a){Z.apply(this,arguments)}c(R,Z);R.prototype.F=function(){this.A.push([]);this.A[0].push({x:-200,y:100});this.A[0].push({x:200,y:100});this.A[0].push({x:200,y:-100});this.A[0].push({x:-200,y:-100});this.name="钉板"};R.prototype.D=function(){for(var a=[-150,-75,0,75,150],b=[-60,-20,20,60],e=0;e<b.length;e++)for(var g=0;g<a.length;g++)Y(new I(a[g],b[e]))};function S(a){Z.apply(this,arguments)}c(S,Z);S.prototype.F=function(){this.A.push([]);for(var a=4*Math.PI/180,b=0;90>b;b++){var e=2*Math.PI-b*a;this.A[0].push({x:150*Math.cos(e),y:150*Math.sin(e)})}this.name="圆形轨道"};S.prototype.D=function(){Y(new I(0,0));Y(new I(0,0,50,90,70));Y(new I(0,0,100,90,70));Y(new I(0,0,50,270,70));Y(new I(0,0,100,270,70))};function T(a){Z.apply(this,arguments)}c(T,Z);T.prototype.F=function(){this.A.push([]);this.A[0].push({x:-60,y:150});this.A[0].push({x:60,y:150});this.A[0].push({x:60,y:-150});this.A[0].push({x:-60,y:-150});this.name="缝衣针"};T.prototype.D=function(){Y(new I(0,0));Y(new I(0,50));Y(new I(0,-50));Y(new F(-40,25,40,0));Y(new F(40,-25,40,0));Y(new F(40,75,40,0));Y(new F(-40,-75,40,0))};function U(a){Z.apply(this,arguments)}c(U,Z);U.prototype.F=function(){this.A.push([]);this.A[0].push({x:-200,y:0});this.A[0].push({x:0,y:200});this.A[0].push({x:200,y:0});this.A[0].push({x:0,y:-200});this.N=this.L=12;this.name="耐心"};U.prototype.D=function(){Y(new F(0,0,250,0,40));Y(new I(0,120));Y(new I(30,90));Y(new I(60,60));Y(new I(90,30));Y(new I(-30,90));Y(new I(-60,60));Y(new I(-90,30));Y(new I(-120,0));Y(new I(-90,-30));Y(new I(-60,-60));Y(new I(-30,-90));Y(new I(0,-120));Y(new I(30,-90));Y(new I(60,-60));Y(new I(90,-30));Y(new I(120,0))};function V(a){Z.apply(this,arguments)}c(V,Z);V.prototype.F=function(){this.A.push([]);this.A[0].push({x:-200,y:200});this.A[0].push({x:-50,y:200});this.A[0].push({x:-50,y:20});this.A[0].push({x:200,y:20});this.A[0].push({x:200,y:-200});this.A[0].push({x:50,y:-200});this.A[0].push({x:50,y:-20});this.A[0].push({x:-200,y:-20});this.name="回旋镖"};V.prototype.D=function(){Y(new I(0,0));Y(new I(-30,0));Y(new I(-60,0));Y(new I(30,0));Y(new I(60,0));Y(new I(90,0));Y(new I(-90,0));Y(new I(120,0));Y(new I(-120,0));Y(new F(-125,160,150));Y(new F(125,-160,150));Y(new I(-125,180));Y(new I(125,-180));Y(new F(-60,40,40,90));Y(new F(60,-40,40,90))};function W(a){Z.apply(this,arguments)}c(W,Z);W.prototype.F=function(){this.A.push([]);this.A[0].push({x:50,y:-100});this.A[0].push({x:-50,y:-100});this.C.push([]);this.C[0].push({x:0,y:1});this.C[0].push({x:0,y:1});this.A.push([]);this.A[1].push({x:-125,y:100});this.A[1].push({x:-25,y:100});this.C.push([]);this.C[1].push({x:0,y:-1});this.C[1].push({x:0,y:-1});this.A.push([]);this.A[2].push({x:125,y:100});this.A[2].push({x:25,y:100});this.C.push([]);this.C[2].push({x:0,y:-1});this.C[2].push({x:0,y:-1});this.name="分割机"};W.prototype.D=function(){Y(new I(-35,-50));Y(new I(-35,-25));Y(new I(-35,0));Y(new I(-35,25));Y(new I(-35,50));Y(new I(35,-50));Y(new I(35,-25));Y(new I(35,0));Y(new I(35,25));Y(new I(35,50))};function X(a){Z.apply(this,arguments)}c(X,Z);X.prototype.F=function(){this.A.push([]);this.A[0].push({x:-250,y:-100});this.A[0].push({x:250,y:-100});this.C.push([]);this.C[0].push({x:0,y:1});this.C[0].push({x:0,y:1});this.A.push([]);this.A[1].push({x:-140,y:100});this.A[1].push({x:-110,y:100});this.C.push([]);this.C[1].push({x:0,y:-1});this.C[1].push({x:0,y:-1});this.A.push([]);this.A[2].push({x:140,y:100});this.A[2].push({x:110,y:100});this.C.push([]);this.C[2].push({x:0,y:-1});this.C[2].push({x:0,y:-1});this.A.push([]);this.A[3].push({x:-15,y:100});this.A[3].push({x:15,y:100});this.C.push([]);this.C[3].push({x:0,y:-1});this.C[3].push({x:0,y:-1});this.N=this.L=12;this.name="三重射击"};X.prototype.D=function(){Y(new I(-125,-50));Y(new I(-125,0));Y(new I(-125,50));Y(new I(0,-50));Y(new I(0,0));Y(new I(0,50));Y(new I(125,-50));Y(new I(125,0));Y(new I(125,50))};function Ia(a){Z.apply(this,arguments)}c(Ia,Z);Ia.prototype.F=function(){this.A.push([]);for(var a=150,b=90,e=360/b*Math.PI/180,g=0;g<b;g++){var h=2*Math.PI-g*e;this.A[0].push({x:Math.cos(h)*a,y:Math.sin(h)*a})}this.A.push([]);a=100;b=45;e=360/b*Math.PI/180;for(g=0;g<b;g++)h=g*e,this.A[1].push({x:Math.cos(h)*a,y:Math.sin(h)*a});this.name="甜甜圈"};Ia.prototype.D=function(){Y(new I(0,115));Y(new I(0,135));Y(new I(0,-115));Y(new I(0,-135));Y(new I(115,0));Y(new I(135,0));Y(new I(-115,0));Y(new I(-135,0));Y(new F(81,81,140,-45));Y(new F(-81,81,140,45));Y(new F(81,-81,140,45));Y(new F(-81,-81,140,-45))};function Ja(a){Z.apply(this,arguments)}c(Ja,Z);Ja.prototype.F=function(){this.A.push([]);this.A[0].push({x:-300,y:100});this.A[0].push({x:-300,y:-100});this.C.push([]);this.C[0].push({x:1,y:0});this.C[0].push({x:1,y:0});this.A.push([]);this.A[1].push({x:300,y:100});this.A[1].push({x:300,y:-100});this.C.push([]);this.C[1].push({x:-1,y:0});this.C[1].push({x:-1,y:0});this.name="遥远"};Ja.prototype.D=function(){Y(new I(-50,0));Y(new I(50,0));Y(new I(100,0));Y(new I(-100,0));Y(new I(200,0));Y(new I(-200,0));Y(new I(250,0));Y(new I(-250,0));Y(new F(0,-100,75,90,0,0,200,1,.5));Y(new F(-150,-100,75,90,0,0,200,1.5,.5));Y(new F(150,-100,75,90,0,0,200,.5,.5))};function Ra(a){Z.apply(this,arguments)}c(Ra,Z);Ra.prototype.F=function(){this.A.push([]);this.A[0].push({x:-300,y:0});this.A[0].push({x:-225,y:0});this.A[0].push({x:-225,y:50});this.A[0].push({x:225,y:50});this.A[0].push({x:225,y:0});this.A[0].push({x:300,y:0});this.A[0].push({x:225,y:0});this.A[0].push({x:225,y:-50});this.A[0].push({x:-225,y:-50});this.A[0].push({x:-225,y:0});this.name="环形赛道"};Ra.prototype.D=function(){for(var a=0;6>a;a++)Y(new I(-125+50*a,30)),Y(new I(-125+50*a,0)),Y(new I(-125+50*a,-30));Y(new F(0,-50,50,90));Y(new F(-50,50,50,90));Y(new F(50,50,50,90));Y(new F(-100,-50,50,90));Y(new F(100,-50,50,90));Y(new F(-150,50,50,90));Y(new F(150,50,50,90))};function Oa(a){Z.apply(this,arguments)}c(Oa,Z);Oa.prototype.F=function(){this.A.push([]);this.A[0].push({x:-225,y:150});this.A[0].push({x:-225,y:50});this.A[0].push({x:-125,y:50});this.A[0].push({x:-125,y:150});this.A.push([]);this.A[1].push({x:175,y:125});this.A[1].push({x:175,y:75});this.A[1].push({x:225,y:75});this.A[1].push({x:225,y:125});this.A.push([]);this.A[2].push({x:150,y:-75});this.A[2].push({x:150,y:-125});this.A[2].push({x:200,y:-125});this.A[2].push({x:200,y:-75});this.A.push([]);this.A[3].push({x:-200,y:-85});this.A[3].push({x:-200,y:-110});this.A[3].push({x:-175,y:-110});this.A[3].push({x:-175,y:-85});this.name="四合院"};Oa.prototype.D=function(){for(var a=0;5>a;a++)Y(new I(-75+50*a,100));for(a=0;6>a;a++)Y(new I(-135+50*a,-97.5));for(a=0;2>a;a++)Y(new I(-187.5,10-50*a));for(a=0;3>a;a++)Y(new I(187.5,50-50*a))};function La(a){Z.apply(this,arguments)}c(La,Z);La.prototype.F=function(){this.A.push([]);this.A[0].push({x:-300,y:100});this.A[0].push({x:-145,y:100});this.A[0].push({x:-135,y:80});this.A[0].push({x:-115,y:80});this.A[0].push({x:-105,y:100});this.A[0].push({x:105,y:100});this.A[0].push({x:115,y:80});this.A[0].push({x:135,y:80});this.A[0].push({x:145,y:100});this.A[0].push({x:300,y:100});this.A[0].push({x:300,y:20});this.A[0].push({x:280,y:10});this.A[0].push({x:280,y:-10});this.A[0].push({x:300,y:-20});this.A[0].push({x:300,y:-100});this.A[0].push({x:145,y:-100});this.A[0].push({x:135,y:-80});this.A[0].push({x:115,y:-80});this.A[0].push({x:105,y:-100});this.A[0].push({x:-105,y:-100});this.A[0].push({x:-115,y:-80});this.A[0].push({x:-135,y:-80});this.A[0].push({x:-145,y:-100});this.A[0].push({x:-300,y:-100});this.A[0].push({x:-300,y:-20});this.A[0].push({x:-280,y:-10});this.A[0].push({x:-280,y:10});this.A[0].push({x:-300,y:20});this.name="剃须刀"};La.prototype.D=function(){for(var a=0;10>a;a++)Y(new I(-225+50*a,0));Y(new I(-125,40));Y(new I(-125,-40));Y(new I(125,40));Y(new I(125,-40))};function Ta(a){Z.apply(this,arguments)}c(Ta,Z);Ta.prototype.F=function(){this.A.push([]);this.C.push([]);for(var a=8*Math.PI/180,b=0;45>b;b++){var e=b*a;this.A[0].push({x:70*Math.cos(e),y:70*Math.sin(e)})}this.A.push([]);this.A[1].push({x:-300,y:50});this.A[1].push({x:-300,y:-50});this.C.push([]);this.C[1].push({x:1,y:0});this.C[1].push({x:1,y:0});this.A.push([]);this.A[2].push({x:215,y:-135});this.A[2].push({x:135,y:-215});this.C.push([]);this.C[2].push({x:-.707,y:.707});this.C[2].push({x:-.707,y:.707});this.A.push([]);this.A[3].push({x:175,y:125});this.A[3].push({x:125,y:175});this.C.push([]);this.C[3].push({x:-.707,y:-.707});this.C[3].push({x:-.707,y:-.707});this.name="异形"};Ta.prototype.D=function(){Y(new I(-112,0));Y(new I(-162,0));Y(new I(-212,0));Y(new I(-262,0));Y(new I(80,-80));Y(new I(110,-110));Y(new I(140,-140));Y(new I(85,85));Y(new I(120,120));Y(new F(-188,150,75,90,0,0,-300,.5,.5));Y(new F(0,205,75,-45,0,215,-215,.5,.5))};function Ka(a){Z.apply(this,arguments)}c(Ka,Z);Ka.prototype.F=function(){this.A.push([]);this.A[0].push({x:-280,y:150});this.A[0].push({x:-280,y:-150});this.A[0].push({x:-260,y:-150});this.A[0].push({x:-260,y:150});this.A.push([]);this.A[1].push({x:-100,y:100});this.A[1].push({x:-100,y:-100});this.A[1].push({x:-80,y:-100});this.A[1].push({x:-80,y:100});this.A.push([]);this.A[2].push({x:80,y:50});this.A[2].push({x:80,y:-50});this.A[2].push({x:100,y:-50});this.A[2].push({x:100,y:50});this.A.push([]);this.A[3].push({x:260,y:25});this.A[3].push({x:260,y:-25});this.A[3].push({x:280,y:-25});this.A[3].push({x:280,y:25});this.name="条隙"};Ka.prototype.D=function(){Y(new I(-130,0));Y(new I(-180,0));Y(new I(-230,0));Y(new I(-130,80));Y(new I(-180,80));Y(new I(-230,80));Y(new I(-130,-80));Y(new I(-180,-80));Y(new I(-230,-80));Y(new I(-50,-30));Y(new I(0,-30));Y(new I(50,-30));Y(new I(-50,30));Y(new I(0,30));Y(new I(50,30));Y(new I(130,0));Y(new I(180,0));Y(new I(230,0))};function Pa(a){Z.apply(this,arguments)}c(Pa,Z);Pa.prototype.F=function(){this.A.push([]);this.A[0].push({x:-275,y:-200});this.A[0].push({x:-250,y:-200});this.C.push([]);this.C[0].push({x:0,y:1});this.C[0].push({x:0,y:1});this.A.push([]);this.A[1].push({x:-275,y:0});this.A[1].push({x:-250,y:25});this.C.push([]);this.C[1].push({x:.707,y:-.707});this.C[1].push({x:.707,y:-.707});this.A.push([]);this.A[2].push({x:-150,y:-200});this.A[2].push({x:-25,y:-200});this.C.push([]);this.C[2].push({x:0,y:1});this.C[2].push({x:0,y:1});this.A.push([]);this.A[3].push({x:-75,y:100});this.A[3].push({x:-50,y:125});this.C.push([]);this.C[3].push({x:.707,y:-.707});this.C[3].push({x:.707,y:-.707});this.A.push([]);this.A[4].push({x:160,y:-200});this.A[4].push({x:285,y:-200});this.C.push([]);this.C[4].push({x:0,y:1});this.C[4].push({x:0,y:1});this.A.push([]);this.A[5].push({x:160,y:180});this.A[5].push({x:285,y:180});this.C.push([]);this.C[5].push({x:0,y:-1});this.C[5].push({x:0,y:-1});this.N=this.L=12;this.name="一波三折"};Pa.prototype.D=function(){for(var a=0;3>a;a++)Y(new I(-262,-150+50*a));for(a=1;4>a;a++)Y(new I(-262+50*a,12-50*a));for(a=0;5>a;a++)Y(new I(-62,-150+50*a));for(a=1;6>a;a++)Y(new I(-62+50*a,112-50*a));for(a=0;7>a;a++)Y(new I(222,-150+50*a));Y(new F(-225,-75,100,0,-180));Y(new F(-12,0,125,0,180));Y(new F(222,50,100,0,0,-100,0,1,.5));Y(new F(222,-50,100,0,0,100,0,1,.5))};function Ma(a){Z.apply(this,arguments)}c(Ma,Z);Ma.prototype.F=function(){this.A.push([]);for(var a=4*Math.PI/180,b=0;22.5>b;b++){var e=1.745*Math.PI-b*a;this.A[0].push({x:300*Math.cos(e),y:300*Math.sin(e)+150})}this.A[0].push({x:-50,y:150});this.A[0].push({x:50,y:150});this.name="贝壳"};Ma.prototype.D=function(){var a=-60,b=95,e=50,g=Math.cos(235*Math.PI/180)*e;e*=Math.sin(235*Math.PI/180);for(var h=0;4>h;h++)Y(new I(-a-g*h,b+e*h)),Y(new I(a+g*h,b+e*h));a=-17;b=85;e=50;g=Math.cos(255*Math.PI/180)*e;e*=Math.sin(255*Math.PI/180);for(h=0;4>h;h++)Y(new I(-a-g*h,b+e*h)),Y(new I(a+g*h,b+e*h));Y(new F(0,0,150,90));Y(new F(75,20,150,-60));Y(new F(-75,20,150,60))};function Qa(a){Z.apply(this,arguments)}c(Qa,Z);Qa.prototype.F=function(){this.A.push([]);this.A[0].push({x:-250,y:0});this.A[0].push({x:-250,y:50});this.A[0].push({x:250,y:50});this.A[0].push({x:-250,y:50});this.C.push([]);this.C[0].push({x:1,y:0});this.C[0].push({x:0,y:-1});this.C[0].push({x:0,y:-1});this.C[0].push({x:1,y:0});this.A.push([]);this.A[1].push({x:250,y:0});this.A[1].push({x:250,y:-50});this.A[1].push({x:-250,y:-50});this.A[1].push({x:250,y:-50});this.C.push([]);this.C[1].push({x:-1,y:0});this.C[1].push({x:0,y:1});this.C[1].push({x:0,y:1});this.C[1].push({x:-1,y:0});this.name="X元素"};Qa.prototype.D=function(){Y(new I(0,-25));Y(new I(0,25));Y(new I(100,-25));Y(new I(100,25));Y(new I(-100,-25));Y(new I(-100,25));Y(new I(200,-25));Y(new I(200,25));Y(new I(-200,-25));Y(new I(-200,25));Y(new F(200,0,80,0,270,-400,0,.75,0));Y(new F(200,0,80,90,270,-400,0,.75,0))};function Sa(a){Z.apply(this,arguments)}c(Sa,Z);Sa.prototype.F=function(){this.A.push([]);this.A[0].push({x:-150,y:150});this.A[0].push({x:-200,y:150});this.A[0].push({x:-200,y:100});this.A[0].push({x:-200,y:150});this.C.push([]);this.C[0].push({x:0,y:-1});this.C[0].push({x:1,y:0});this.C[0].push({x:1,y:0});this.C[0].push({x:0,y:-1});this.A.push([]);this.A[1].push({x:-150,y:0});this.A[1].push({x:-200,y:0});this.A[1].push({x:-200,y:50});this.A[1].push({x:-200,y:0});this.C.push([]);this.C[1].push({x:0,y:1});this.C[1].push({x:1,y:0});this.C[1].push({x:1,y:0});this.C[1].push({x:0,y:1});this.A.push([]);this.A[2].push({x:150,y:50});this.A[2].push({x:200,y:50});this.A[2].push({x:200,y:0});this.A[2].push({x:200,y:50});this.C.push([]);this.C[2].push({x:0,y:-1});this.C[2].push({x:-1,y:0});this.C[2].push({x:-1,y:0});this.C[2].push({x:0,y:-1});this.A.push([]);this.A[3].push({x:150,y:-100});this.A[3].push({x:200,y:-100});this.A[3].push({x:200,y:-50});this.A[3].push({x:200,y:-100});this.C.push([]);this.C[3].push({x:0,y:1});this.C[3].push({x:-1,y:0});this.C[3].push({x:-1,y:0});this.C[3].push({x:0,y:1});this.A.push([]);this.A[4].push({x:-150,y:-50});this.A[4].push({x:-200,y:-50});this.A[4].push({x:-200,y:-100});this.A[4].push({x:-200,y:-50});this.C.push([]);this.C[4].push({x:0,y:-1});this.C[4].push({x:1,y:0});this.C[4].push({x:1,y:0});this.C[4].push({x:0,y:-1});this.A.push([]);this.A[5].push({x:-150,y:-200});this.A[5].push({x:-200,y:-200});this.A[5].push({x:-200,y:-150});this.A[5].push({x:-200,y:-200});this.C.push([]);this.C[5].push({x:0,y:1});this.C[5].push({x:1,y:0});this.C[5].push({x:1,y:0});this.C[5].push({x:0,y:1});this.A.push([]);this.A[6].push({x:150,y:-200});this.A[6].push({x:200,y:-200});this.A[6].push({x:200,y:-150});this.A[6].push({x:200,y:-200});this.C.push([]);this.C[6].push({x:0,y:1});this.C[6].push({x:-1,y:0});this.C[6].push({x:-1,y:0});this.C[6].push({x:0,y:1});this.N=this.L=12;this.name="曲折前行"};Sa.prototype.D=function(){Y(new I(-175,125));Y(new I(-175,75));Y(new I(-175,25));for(var a=0;7>a;a++)Y(new I(-125+50*a,25)),Y(new I(-125+50*a,-75)),Y(new I(-125+50*a,-175));Y(new I(175,-25));Y(new I(-175,-75));Y(new I(-175,-125));Y(new I(-175,-175));Y(new F(0,-25,150,0,180))};function Na(a){Z.apply(this,arguments)}c(Na,Z);Na.prototype.F=function(){this.A.push([]);this.A[0].push({x:-100,y:100});this.A[0].push({x:100,y:100});this.A[0].push({x:100,y:-100});this.A[0].push({x:-100,y:-100});this.name="复仇盒子"};Na.prototype.D=function(){Y(new I(0,0));Y(new I(-50,0));Y(new I(50,0));Y(new I(-25,0));Y(new I(25,0));Y(new I(0,50));Y(new I(-50,50));Y(new I(50,50));Y(new I(-25,50));Y(new I(25,50));Y(new I(0,-50));Y(new I(-50,-50));Y(new I(50,-50));Y(new I(-25,-50));Y(new I(25,-50));Y(new F(-32,32,50,0,180));Y(new F(38,-50,50,90,0,0,50,1,.5))};function Za(){var a=q,b=u;this.canvas=document.createElement("canvas");this.canvas.setAttribute("width",a);this.canvas.setAttribute("height",b);this.canvas.style.width=1*a+"px";this.canvas.style.height=1*b+"px";this.canvas.style.backgroundColor="black";document.getElementById("game").appendChild(this.canvas);this.B=this.canvas.getContext("2d");this.width=a;this.height=b;this.scale=1;this.entities=[];this.Fa=this.qa=!1;$a(this);ab(this);bb(this);this.Ga(performance.now())}function bb(a){a.I={};[].forEach(function(b){a.I[b]={};a.I[b].loaded=!1;b.endsWith(".png")||b.endsWith(".jpg")?(a.I[b].data=new Image,a.I[b].data.onload=function(){return a.I[b].loaded=!0},a.I[b].data.src=b):b.endsWith(".wav")||b.endsWith(".mp3")?(a.I[b].data=new Audio,a.I[b].data.src=b,a.I[b].data.load(),a.I[b].loaded=!0):console.assert(!1,"Unable to load "+b+" - unknown type")})}function cb(a){return 0<Object.keys(a.I).length&&0==Object.values(a.I).every(function(a){return a.loaded})}Za.prototype.Ga=function(a){window.requestAnimationFrame(this.Ga.bind(this));if(!cb(this)){var b=Math.min((a-(this.gb||a))/1E3,.2);this.gb=a;this.B.clearRect(-this.width,-this.height,2*this.width,2*this.height);void 0!==this.state&&this.state(b);db(this);eb(this,b);fb(this);void 0!==this.la&&this.la(b);gb(this)}};function Y(a){var b=p;Object.defineProperty(a,"z",{set:function(e){a.Da=e;b.qa=!0},get:function(){return a.Da}});a.Da=0<b.entities.length?b.entities[b.entities.length-1].z+1:0;b.entities.push(a)}function eb(a,b){a.entities.forEach(function(a){void 0!==a.update&&a.update(b)});a.Fa&&(a.entities=a.entities.filter(function(a){return!0!==a.S}),a.Fa=!1)}function fb(a){a.entities.forEach(function(a){void 0!==a.ca&&a.ca()})}function db(a){a.qa&&(a.entities.sort(function(a,e){return a.z-e.z}),a.qa=!1)}function K(a){var b=p,e=void 0!==a.angle?a.angle*Math.PI/180:0,g=void 0!==a.bb?a.bb:"Arial",h=void 0!==a.fontSize?a.fontSize:12,m=void 0!==a.fontStyle?a.fontStyle:"",r=void 0!==a.color?a.color:"#FFF",t=void 0!==a.textAlign?a.textAlign.toLowerCase():"left",n=void 0!==a.textBaseline?a.textBaseline.toLowerCase():"bottom";b.B.save();b.B.translate(a.x,a.y);b.B.rotate(e);b.B.font=m+" "+h+"px "+g;b.B.fillStyle=r;b.B.textAlign=t;b.B.textBaseline=n;b.B.fillText(a.text,0,0);b.B.restore()}function ab(a){a.ka=!0;a.jb={c:16.35,"c#":17.32,d:18.35,"d#":19.45,e:20.6,f:21.83,"f#":23.12,g:24.5,"g#":25.96,a:27.5,"a#":29.14,b:30.87};window.addEventListener("click",function(){if(a.G)a.G.resume();else{a.G=new (window.AudioContext||window.webkitAudioContext);var b=12*a.G.sampleRate;a.Oa=a.G.createBuffer(1,b,a.G.sampleRate);a.ib=a.Oa.getChannelData(0);for(var e=0;e<b;e++)a.ib[e]=-1+2*Math.random()}})}function H(a,b,e,g,h){var m=p;if(m.ka&&m.G){var r=m.G.createOscillator();a=m.jb[a.toLowerCase()];void 0!==b&&(a*=Math.pow(2,b));r.type=void 0!==h?h:"sine";r.frequency.setValueAtTime(a,m.G.currentTime);void 0!==e&&(e*=2);void 0!==g&&(g*=2);r.connect(m.G.destination);r.start(m.G.currentTime+(void 0!==g?g:0));r.stop(m.G.currentTime+(void 0!==g?g:0)+(void 0!==e?e:.2))}}function $a(a){a.aa={x:0,y:0};a.X={x:0,y:0};a.Ka=!1;a.La=!1;a.M=!1;a.Ma=!1;window.addEventListener("mousemove",function(b){a.X.x+=b.kb;a.X.y+=b.lb;var e=a.canvas.getBoundingClientRect();a.aa={x:b.clientX-e.left,y:b.clientY-e.top}});window.addEventListener("mousedown",function(b){0===b.button?(a.Ka=!0,a.M=!0):2===b.button&&(a.La=!0,a.Ma=!0)});window.addEventListener("mouseup",function(b){0===b.button?a.Ka=!1:2===b.button&&(a.La=!1)});window.addEventListener("touchstart",a.ua,!0);window.addEventListener("touchmove",a.ua,!0);window.addEventListener("touchend",a.ua,!0);a.ta={a:"a",b:"b",c:"c",d:"d",e:"e",f:"f",g:"g",h:"h",i:"i",j:"j",k:"k",l:"l",m:"m",n:"n",o:"o",p:"p",q:"q",r:"r",s:"s",t:"t",u:"u",v:"v",w:"w",x:"x",y:"y",z:"z",0:"zero",1:"one",2:"two",3:"three",4:"four",5:"five",6:"six",7:"seven",8:"eight",9:"nine",arrowup:"up",arrowdown:"down",arrowleft:"left",arrowright:"right"," ":"space",escape:"escape",control:"ctrl",shift:"shift",alt:"alt",tab:"tab",enter:"enter",backspace:"backspace"};a.keys={};a.W={};Object.keys(a.ta).forEach(function(b){return a.keys[b]=!1});window.addEventListener("keydown",function(b){hb(a,b,!0)});window.addEventListener("keyup",function(b){hb(a,b,!1)})}Za.prototype.ua=function(a){var b=a.changedTouches[0];switch(a.type){case "touchstart":var e="mousedown";break;case "touchend":e="mouseup";break;case "touchmove":e="mousemove";break;default:return}var g=document.createEvent("MouseEvent");g.initMouseEvent(e,!0,!0,window,1,b.screenX,b.screenY,b.clientX,b.clientY,!1,!1,!1,!1,0,null);b.target.dispatchEvent(g);a.preventDefault()};function hb(a,b,e){var g=b.key.toLowerCase();void 0!==a.ta[g]&&(g=a.ta[g],a.W[g]=!1===a.keys[g]||void 0===a.keys[g],a.keys[g]=e,"up"!==g&&"down"!==g&&"left"!==g&&"right"!==g||b.preventDefault())}function gb(a){a.X.x=0;a.X.y=0;a.M=!1;a.Ma=!1;Object.keys(a.W).forEach(function(b){a.W[b]=!1})}var q=640,u=480,p=new Za;p.state=Ya;var E,P,L=0,Ha=0,J=5,l=0;function Ya(a){O(a);p.M&&(p.state=N,p.M=!1,H("a",4,.05,0),H("b",4,.05,.05));p.B.shadowBlur=20;p.B.shadowColor="#08F";K({text:"开始游戏",x:.5*q,y:.5*u,fontSize:20,fontStyle:"bold",color:"#08F",textAlign:"center"})};</script></body></html>'''
        html5 = '''<!DOCTYPE html><html lang="cn" ><head><meta charset="UTF-8"><title>排排坐</title><meta name="viewport" content="width=device-width, initial-scale=1"><style type="text/css">button,hr,input{overflow:visible}audio,canvas,progress,video{display:inline-block}progress,sub,sup{vertical-align:baseline}html{font-family:sans-serif;line-height:1.15;-ms-text-size-adjust:100%;-webkit-text-size-adjust:100%}body{margin:0} menu,article,aside,details,footer,header,nav,section{display:block}h1{font-size:2em;margin:.67em 0}figcaption,figure,main{display:block}figure{margin:1em 40px}hr{box-sizing:content-box;height:0}code,kbd,pre,samp{font-family:monospace,monospace;font-size:1em}a{background-color:transparent;-webkit-text-decoration-skip:objects}a:active,a:hover{outline-width:0}abbr[title]{border-bottom:none;text-decoration:underline;text-decoration:underline dotted}b,strong{font-weight:bolder}dfn{font-style:italic}mark{background-color:#ff0;color:#000}small{font-size:80%}sub,sup{font-size:75%;line-height:0;position:relative}sub{bottom:-.25em}sup{top:-.5em}audio:not([controls]){display:none;height:0}img{border-style:none}svg:not(:root){overflow:hidden}button,input,optgroup,select,textarea{font-family:sans-serif;font-size:100%;line-height:1.15;margin:0}button,input{}button,select{text-transform:none}[type=submit], [type=reset],button,html [type=button]{-webkit-appearance:button}[type=button]::-moz-focus-inner,[type=reset]::-moz-focus-inner,[type=submit]::-moz-focus-inner,button::-moz-focus-inner{border-style:none;padding:0}[type=button]:-moz-focusring,[type=reset]:-moz-focusring,[type=submit]:-moz-focusring,button:-moz-focusring{outline:ButtonText dotted 1px}fieldset{border:1px solid silver;margin:0 2px;padding:.35em .625em .75em}legend{box-sizing:border-box;color:inherit;display:table;max-width:100%;padding:0;white-space:normal}progress{}textarea{overflow:auto}[type=checkbox],[type=radio]{box-sizing:border-box;padding:0}[type=number]::-webkit-inner-spin-button,[type=number]::-webkit-outer-spin-button{height:auto}[type=search]{-webkit-appearance:textfield;outline-offset:-2px}[type=search]::-webkit-search-cancel-button,[type=search]::-webkit-search-decoration{-webkit-appearance:none}::-webkit-file-upload-button{-webkit-appearance:button;font:inherit}summary{display:list-item}[hidden],template{display:none}/*# sourceMappingURL=normalize.min.css.map */body,html{height:100%;margin:0;padding:1rem;font-size:18px;background:#f5f5f5;box-sizing:border-box;overflow:hidden}.game{position:relative;display:flex;flex-direction:column;height:100%;max-width:400px;margin:0 auto}.game-header{display:flex;padding:1rem;white-space:nowrap;color:#fff;background:#000}.game-score{margin-left:auto}.game-score em{font-style:normal;font-weight:bold}.game-canvas{display:flex;flex-direction:column;justify-content:center;justify-content:space-around;padding:0.6rem 0;flex-grow:2;background:#fff;overflow:hidden;text-align:center}.game-canvas .row{display:flex;justify-content:space-between;padding:0.3em 1rem 0.3rem 1rem}.game-menu{display:flex;padding:1rem;color:#fff;background:black;justify-content:space-between}button{color:#fff;background:transparent;border:0;padding:0;cursor:pointer}button:focus{outline:none}@media (max-width:800px){.game-canvas{pointer-events:none}}@media (max-width:500px){body,html{font-size:16px;padding:0}}</style></head><body><div class="game"><header class="game-header"><span class="game-status">&nbsp;</span><span class="game-score"></span></header><div class="game-canvas"></div><footer class="game-menu"><button class="restart">重新开始</button><button class="mode">简单</button></footer></div><script>const COLUMNS=18;const ROW_TEMPLATE='<input type="checkbox"/>'.repeat(COLUMNS);const easy={currentScore:0,currentRow:1,currentMultiplier:1,currentSpeed:1000,currentWidth:6};const hard={...easy,currentMultiplier:3,currentSpeed:600,currentWidth:4};let currentSettings=easy;let game=document.querySelector('.game');let canvas=document.querySelector('.game-canvas');let status=document.querySelector('.game-status');let score=document.querySelector('.game-score');let modeButton=document.querySelector('.mode');let restartButton=document.querySelector('.restart');let rows;let rowHeight;let state;let startTime;window.onresize=resize;restartButton.onmousedown=reset;modeButton.onmousedown=toggleMode;document.onkeydown=event=>{if(event.keyCode===32)click(event);if(event.keyCode===82)reset()};if('ontouchstart'in window){window.ontouchstart=click}else{window.onmousedown=click};build();reset();paint();function reset(){setState('playing');rows.forEach(row=>row.forEach(box=>box.checked=false));startTime=Date.now();({currentRow,currentSpeed,currentWidth,currentScore,currentMultiplier}=currentSettings);selectBoxes({row:0,index:Math.floor(COLUMNS/2-currentWidth/2),width:currentWidth});score.innerHTML='得分 <em>'+currentScore+'</em>'};function resize(){if(build())reset()};function click(event){if(!event.type.startsWith('key')&&event.target.matches('a, button'))return;event.preventDefault();if(state==='playing'){step()}else{reset()}};function setState(value){state=value;if(state==='playing')status.textContent='按空格或点击鼠标开始游戏';else if(state==='won')status.textContent='你真棒 🏅✌️🦄';else if(state==='lost')status.textContent='失败 💥'};function toggleMode(){if(/简单/i.test(modeButton.textContent)){currentSettings=hard;modeButton.textContent='困难'}else{currentSettings=easy;modeButton.textContent='简单'}reset()};function build(){let canvasHeight=canvas.offsetHeight;if(typeof rowHeight==='number'&&rows.length===Math.floor(canvasHeight/rowHeight)-1){return false}rows=[];canvas.innerHTML='';let firstRow=generateRow();rowHeight=firstRow.offsetHeight;Array(Math.floor(canvasHeight/rowHeight)-2).fill().map(generateRow);return true};function generateRow(){let row=document.createElement('div');row.className='row';row.innerHTML=ROW_TEMPLATE;canvas.appendChild(row);rows.unshift(Array.from(row.childNodes));return row};function selectBoxes({row=currentRow,index,width}){rows[row].forEach((box,i)=>box.checked=i>=index&&i<=index+width-1)};function step(){currentWidth=0;rows[currentRow].forEach((box,i)=>{if(box.checked&&rows[currentRow-1][i].checked){currentWidth+=1}});currentRow+=1;let multiplier=currentMultiplier*(1+(currentRow/rows.length));currentScore=Math.ceil(currentScore+currentWidth*multiplier);if(currentWidth===0){setState('lost')}else if(currentRow>=rows.length){currentScore+=30*multiplier;setState('won')}score.innerHTML='得分 <em>'+currentScore+'</em>'};function paint(){if(state==='playing'){let time=(Date.now()-startTime)%(currentSpeed*2);if(time>currentSpeed)time=currentSpeed*2-time;selectBoxes({index:Math.floor(time/currentSpeed*(COLUMNS-currentWidth+1)),width:currentWidth})}requestAnimationFrame(paint)}</script></body></html>'''
        html6 = '''<!DOCTYPE html><html lang="cn"><head><meta charset="UTF-8"><title>棍子英雄</title><style type="text/css">html, body {height: 100%;margin: 0;}body {font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;cursor: pointer;}.container {display: flex;justify-content: center;align-items: center;height: 100%;}#score {position: absolute;top: 30px;right: 30px;font-size: 2em;font-weight: 900;}#introduction {width: 260px;height: 150px;position: absolute;font-weight: 600;font-size: 0.8em;font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;text-align: center;transition: opacity 2s;}#restart {width: 120px;height: 120px;position: absolute;border-radius: 50%;color: white;background-color: red;border: none;font-weight: 700;font-size: 1.2em;font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;display: none;cursor: pointer;}#perfect {position: absolute;opacity: 0;transition: opacity 2s;}</style></head><body><div class="container"><div id="score"></div><canvas id="game" width="375" height="375"></canvas><div id="introduction">长按鼠标伸出棍子，松开鼠标放下棍子。</div><div id="perfect">GOOD！双倍积分！</div><button id="restart">重新开始</button></div><script type="text/javascript">Array.prototype.last=function(){return this[this.length-1]},Math.sinus=function(t){return Math.sin(t/180*Math.PI)};let lastTimestamp,heroX,heroY,sceneOffset,phase="waiting",platforms=[],sticks=[],trees=[],score=0;const canvasWidth=375,canvasHeight=375,platformHeight=100,heroDistanceFromEdge=10,paddingX=100,perfectAreaSize=10,backgroundSpeedMultiplier=.2,hill1BaseHeight=100,hill1Amplitude=10,hill1Stretch=1,hill2BaseHeight=70,hill2Amplitude=20,hill2Stretch=.5,stretchingSpeed=4,turningSpeed=4,walkingSpeed=4,transitioningSpeed=2,fallingSpeed=2,heroWidth=17,heroHeight=30,canvas=document.getElementById("game");canvas.width=window.innerWidth,canvas.height=window.innerHeight;const ctx=canvas.getContext("2d"),introductionElement=document.getElementById("introduction"),perfectElement=document.getElementById("perfect"),restartButton=document.getElementById("restart"),scoreElement=document.getElementById("score");function resetGame(){phase="waiting",lastTimestamp=void 0,sceneOffset=0,score=0,introductionElement.style.opacity=1,perfectElement.style.opacity=0,restartButton.style.display="none",scoreElement.innerText=score,platforms=[{x:50,w:50}],generatePlatform(),generatePlatform(),generatePlatform(),generatePlatform(),sticks=[{x:platforms[0].x+platforms[0].w,length:0,rotation:0}],trees=[],generateTree(),generateTree(),generateTree(),generateTree(),generateTree(),generateTree(),generateTree(),generateTree(),generateTree(),generateTree(),heroX=platforms[0].x+platforms[0].w-heroDistanceFromEdge,heroY=0,draw()}function generateTree(){const t=trees[trees.length-1];const e=(t?t.x:0)+30+Math.floor(120*Math.random()),i=["#6D8821","#8FAC34","#98B333"][Math.floor(3*Math.random())];trees.push({x:e,color:i})}function generatePlatform(){const t=platforms[platforms.length-1];const e=t.x+t.w+40+Math.floor(160*Math.random()),i=20+Math.floor(80*Math.random());platforms.push({x:e,w:i})}function animate(t){if(!lastTimestamp)return lastTimestamp=t,void window.requestAnimationFrame(animate);switch(phase){case"waiting":return;case"stretching":sticks.last().length+=(t-lastTimestamp)/stretchingSpeed;break;case"turning":if(sticks.last().rotation+=(t-lastTimestamp)/turningSpeed,sticks.last().rotation>90){sticks.last().rotation=90;const[t,e]=thePlatformTheStickHits();t&&(score+=e?2:1,scoreElement.innerText=score,e&&(perfectElement.style.opacity=1,setTimeout(()=>perfectElement.style.opacity=0,1e3)),generatePlatform(),generateTree(),generateTree()),phase="walking"}break;case"walking":{heroX+=(t-lastTimestamp)/walkingSpeed;const[e]=thePlatformTheStickHits();if(e){const t=e.x+e.w-heroDistanceFromEdge;heroX>t&&(heroX=t,phase="transitioning")}else{const t=sticks.last().x+sticks.last().length+heroWidth;heroX>t&&(heroX=t,phase="falling")}break}case"transitioning":{sceneOffset+=(t-lastTimestamp)/transitioningSpeed;const[e]=thePlatformTheStickHits();sceneOffset>e.x+e.w-paddingX&&(sticks.push({x:e.x+e.w,length:0,rotation:0}),phase="waiting");break}case"falling":{sticks.last().rotation<180&&(sticks.last().rotation+=(t-lastTimestamp)/turningSpeed),heroY+=(t-lastTimestamp)/fallingSpeed;const e=platformHeight+100+(window.innerHeight-canvasHeight)/2;if(heroY>e)return void(restartButton.style.display="block");break}default:throw Error("Wrong phase")}draw(),window.requestAnimationFrame(animate),lastTimestamp=t}function thePlatformTheStickHits(){if(90!=sticks.last().rotation)throw Error(`Stick is ${sticks.last().rotation}°`);const t=sticks.last().x+sticks.last().length,e=platforms.find(e=>e.x<t&&t<e.x+e.w);return e&&e.x+e.w/2-perfectAreaSize/2<t&&t<e.x+e.w/2+perfectAreaSize/2?[e,!0]:[e,!1]}function draw(){ctx.save(),ctx.clearRect(0,0,window.innerWidth,window.innerHeight),drawBackground(),ctx.translate((window.innerWidth-canvasWidth)/2-sceneOffset,(window.innerHeight-canvasHeight)/2),drawPlatforms(),drawHero(),drawSticks(),ctx.restore()}function drawPlatforms(){platforms.forEach(({x:t,w:e})=>{ctx.fillStyle="black",ctx.fillRect(t,canvasHeight-platformHeight,e,platformHeight+(window.innerHeight-canvasHeight)/2),sticks.last().x<t&&(ctx.fillStyle="red",ctx.fillRect(t+e/2-perfectAreaSize/2,canvasHeight-platformHeight,perfectAreaSize,perfectAreaSize))})}function drawHero(){ctx.save(),ctx.fillStyle="black",ctx.translate(heroX-heroWidth/2,heroY+canvasHeight-platformHeight-heroHeight/2),drawRoundedRect(-heroWidth/2,-heroHeight/2,heroWidth,heroHeight-4,5);ctx.beginPath(),ctx.arc(5,11.5,3,0,2*Math.PI,!1),ctx.fill(),ctx.beginPath(),ctx.arc(-5,11.5,3,0,2*Math.PI,!1),ctx.fill(),ctx.beginPath(),ctx.fillStyle="white",ctx.arc(5,-7,3,0,2*Math.PI,!1),ctx.fill(),ctx.fillStyle="red",ctx.fillRect(-heroWidth/2-1,-12,heroWidth+2,4.5),ctx.beginPath(),ctx.moveTo(-9,-14.5),ctx.lineTo(-17,-18.5),ctx.lineTo(-14,-8.5),ctx.fill(),ctx.beginPath(),ctx.moveTo(-10,-10.5),ctx.lineTo(-15,-3.5),ctx.lineTo(-5,-7),ctx.fill(),ctx.restore()}function drawRoundedRect(t,e,i,n,r){ctx.beginPath(),ctx.moveTo(t,e+r),ctx.lineTo(t,e+n-r),ctx.arcTo(t,e+n,t+r,e+n,r),ctx.lineTo(t+i-r,e+n),ctx.arcTo(t+i,e+n,t+i,e+n-r,r),ctx.lineTo(t+i,e+r),ctx.arcTo(t+i,e,t+i-r,e,r),ctx.lineTo(t+r,e),ctx.arcTo(t,e,t,e+r,r),ctx.fill()}function drawSticks(){sticks.forEach(t=>{ctx.save(),ctx.translate(t.x,canvasHeight-platformHeight),ctx.rotate(Math.PI/180*t.rotation),ctx.beginPath(),ctx.lineWidth=2,ctx.moveTo(0,0),ctx.lineTo(0,-t.length),ctx.stroke(),ctx.restore()})}function drawBackground(){var t=ctx.createLinearGradient(0,0,0,window.innerHeight);t.addColorStop(0,"#BBD691"),t.addColorStop(1,"#FEF1E1"),ctx.fillStyle=t,ctx.fillRect(0,0,window.innerWidth,window.innerHeight),drawHill(hill1BaseHeight,hill1Amplitude,hill1Stretch,"#95C629"),drawHill(hill2BaseHeight,hill2Amplitude,hill2Stretch,"#659F1C"),trees.forEach(t=>drawTree(t.x,t.color))}function drawHill(t,e,i,n){ctx.beginPath(),ctx.moveTo(0,window.innerHeight),ctx.lineTo(0,getHillY(0,t,e,i));for(let n=0;n<window.innerWidth;n++)ctx.lineTo(n,getHillY(n,t,e,i));ctx.lineTo(window.innerWidth,window.innerHeight),ctx.fillStyle=n,ctx.fill()}function drawTree(t,e){ctx.save(),ctx.translate((-sceneOffset*backgroundSpeedMultiplier+t)*hill1Stretch,getTreeY(t,hill1BaseHeight,hill1Amplitude));ctx.fillStyle="#7D833C",ctx.fillRect(-1,-5,2,5),ctx.beginPath(),ctx.moveTo(-5,-5),ctx.lineTo(0,-30),ctx.lineTo(5,-5),ctx.fillStyle=e,ctx.fill(),ctx.restore()}function getHillY(t,e,i,n){const r=window.innerHeight-e;return Math.sinus((sceneOffset*backgroundSpeedMultiplier+t)*n)*i+r}function getTreeY(t,e,i){const n=window.innerHeight-e;return Math.sinus(t)*i+n}resetGame(),resetGame(),window.addEventListener("keydown",function(t){if(" "==t.key)return t.preventDefault(),void resetGame()}),window.addEventListener("mousedown",function(t){"waiting"==phase&&(lastTimestamp=void 0,introductionElement.style.opacity=0,phase="stretching",window.requestAnimationFrame(animate))}),window.addEventListener("mouseup",function(t){"stretching"==phase&&(phase="turning")}),window.addEventListener("resize",function(t){canvas.width=window.innerWidth,canvas.height=window.innerHeight,draw()}),window.requestAnimationFrame(animate),restartButton.addEventListener("click",function(t){t.preventDefault(),resetGame(),restartButton.style.display="none"});</script></body></html>'''
        html7 = '''<!DOCTYPE html><html lang="cn"><head><meta charset="UTF-8"><title>生成零</title><style type="text/css">* {box-sizing: border-box;-moz-box-sizing: border-box;-webkit-box-sizing: border-box;}body {background: #000;margin: 0;overflow: hidden;user-select: none;-moz-user-select: none;-webkit-user-select: none;}#game {position: absolute;width: 100vw;height: 100vh;}.tile {position: absolute;border-radius: 5px;transition: top 0.3s linear, left 0.1s linear, opacity 0.1s linear, background-color 0.5s linear;font-family: 'Julius Sans One', sans-serif;font-size: 8vh;line-height: 8vh;text-align: center;text-overflow: hidden;overflow: hidden;padding: 1vh;width: 10vw;height: 10vh;background: #000;color: #000;border: 1px solid black;cursor: pointer;}.sel {background: #fff!important;}.yh {top:-10vh;}.y0 {top: 0 ;}.x0 {left: 0 ;}.y1 {top: 10vh;}.x1 {left: 10vw;}.y2 {top: 20vh;}.x2 {left: 20vw;}.y3 {top: 30vh;}.x3 {left: 30vw;}.y4 {top: 40vh;}.x4 {left: 40vw;}.y5 {top: 50vh;}.x5 {left: 50vw;}.y6 {top: 60vh;}.x6 {left: 60vw;}.y7 {top: 70vh;}.x7 {left: 70vw;}.y8 {top: 80vh;}.x8 {left: 80vw;}.y9 {top: 90vh;}.x9 {left: 90vw;}.fade-out {opacity:0;}button {appearance: none;border: none;font: inherit;padding: 0;margin: 0;&:focus-visible {z-index: 10;outline: 4px solid #fff;}}</style></head><body><div id=game></div><script>function tile(t,e,n,o){return(o=document.createElement("button")).setPos=function(t,e){o.pos={x:t,y:e},o.setAttribute("class","tile x"+t+" y"+(e<0?"h":e))},o.setVal=function(t){o.textContent=t,o.style.backgroundColor="hsl("+100*t%360+",100%,"+(20+5*t)+"%)"},o.setVal(n),o.setPos(t,e),o}function removeTile(t,e,n,o){t.classList.add("fade-out"),setTimeout(function(){try{game.removeChild(t)}catch(t){console.log(t.message)}e&&e()},100)}function getAdjacentTiles(t,e,n,o,i,s,l,c){for(l=[],s=t.textContent,c=4,i="01211012";c--;)o=[i[2*c]-1,i[2*c+1]-1],(n=$T(t.pos.x+o[0],t.pos.y+o[1]))&&n!=e&&n.textContent==s&&!n.classList.contains("sel")&&(n.classList.add("sel"),l.push(n),[].push.apply(l,getAdjacentTiles(n,e||t)));return l}function interAction(t,e,n,o){game.classList.contains("lock")||$$(".sel").length>0||(o=0|t.textContent)>0&&(e=getAdjacentTiles(t)).length>0&&(moves++,lock(!0),function n(){if(e.length>0)return removeTile(e.pop(),n);t.setVal(o-1),function t(e,n,o,i,s){for(n=0,i=8;i>=-1;i--)for(o=10;o--;)(s=$T(o,i))&&!$T(o,i+1)&&(s.setPos(o,i+1),n++);if(n>0)return setTimeout(function(){t(e)},200);if(e>0){for(o=10;o--;)!$T(o,0)&&R()<.5&&game.appendChild(tile(o,-1,7+3*R()|0));setTimeout(function(){t(e-1)},200)}lock(!1)}(1)}())}for(R=Math.random,d=document,moves=0,$=function(t,e){return(e||d).querySelector(t)},$$=function(t,e){return[].slice.call((e||d).querySelectorAll(t))},$T=function(t,e){return $(".tile.x"+t+".y"+(e<0?"h":e))},lock=function(t){game.classList[t?"add":"remove"]("lock")},i=10;i--;)for(j=10;j--;)game.appendChild(tile(i,j,7+3*R()|0));window.onclick=function(t){t.target.classList.contains("tile")&&interAction(t.target)};</script></body></html>'''
        return random.choice([html1, html2, html3, html4, html5, html6, html7])
        
    @app.errorhandler(404)
    def page_not_found(e):
        return '''<!DOCTYPE html><html><head><meta charset="utf-8"><title>页面未找到</title><style type="text/css">html,body{margin:0;padding:0;height:100%;min-height:450px;font-family:"Dosis",sans-serif;font-size:32px;font-weight:500;color:#5d7399}.content{height:100%;position:relative;z-index:1;background-color:#d2e1ec;background-image:linear-gradient(to bottom,#bbcfe1 0%,#e8f2f6 80%);overflow:hidden}.snow{position:absolute;top:0;left:0;pointer-events:none;z-index:20}.main-text{padding:20vh 20px 0 20px;text-align:center;line-height:2em;font-size:5vh}.home-link{font-size:0.6em;font-weight:400;color:inherit;text-decoration:none;opacity:0.6;border-bottom:1px dashed rgba(93,115,153,0.5)}.home-link:hover{opacity:1}.ground{height:160px;width:100%;position:absolute;bottom:0;left:0;background:#f6f9fa;box-shadow:0 0 10px 10px#f6f9fa}.ground:before,.ground:after{content:"";display:block;width:250px;height:250px;position:absolute;top:-62.5px;z-index:-1;background:transparent;transform:scaleX(0.2)rotate(45deg)}.ground:after{left:50%;margin-left:-166.6666666667px;box-shadow:-340px 260px 15px#bac4d5,-625px 575px 15px#91a1bc,-855px 945px 15px#7e90b0,-1165px 1235px 15px#b0bccf,-1470px 1530px 15px#94a3be,-1750px 1850px 15px#91a1bc,-2145px 2055px 15px#b0bccf,-2400px 2400px 15px#7e90b0,-2665px 2735px 15px#a7b4c9,-2965px 3035px 15px#8496b4,-3260px 3340px 15px#94a3be,-3580px 3620px 15px#97a6c0,-3885px 3915px 15px#9aa9c2,-4160px 4240px 15px#8193b2,-4470px 4530px 15px#8e9eba,-4845px 4755px 15px#7e90b0}.ground:before{right:50%;margin-right:-166.6666666667px;box-shadow:260px-340px 15px#b0bccf,630px-570px 15px#a1aec6,925px-875px 15px#94a3be,1170px-1230px 15px#a7b4c9,1535px-1465px 15px#a7b4c9,1845px-1755px 15px#8a9bb8,2150px-2050px 15px#b7c1d3,2445px-2355px 15px#8798b6,2735px-2665px 15px#bac4d5,3015px-2985px 15px#94a3be,3270px-3330px 15px#b7c1d3,3620px-3580px 15px#8193b2,3860px-3940px 15px#9dabc4,4215px-4185px 15px#8798b6,4485px-4515px 15px#8e9eba,4810px-4790px 15px#bac4d5}.mound{margin-top:-100px;font-weight:800;font-size:180px;text-align:center;color:#dd4040;pointer-events:none}.mound:before{content:"";display:block;width:600px;height:200px;position:absolute;left:50%;margin-left:-300px;top:50px;z-index:1;border-radius:100%;background-color:#e8f2f6;background-image:linear-gradient(to bottom,#dee8f1,#f6f9fa 60px)}.mound:after{content:"";display:block;width:28px;height:6px;position:absolute;left:50%;margin-left:-150px;top:68px;z-index:2;background:#dd4040;border-radius:100%;transform:rotate(-15deg);box-shadow:-56px 12px 0 1px#dd4040,-126px 6px 0 2px#dd4040,-196px 24px 0 3px#dd4040}.mound_text{transform:rotate(10deg)}.mound_spade{display:block;width:35px;height:30px;position:absolute;right:50%;top:42%;margin-right:-250px;z-index:0;transform:rotate(35deg);background:#dd4040}.mound_spade:before,.mound_spade:after{content:"";display:block;position:absolute}.mound_spade:before{width:40%;height:30px;bottom:98%;left:50%;margin-left:-20%;background:#dd4040}.mound_spade:after{width:100%;height:30px;top:-55px;left:0%;box-sizing:border-box;border:10px solid#dd4040;border-radius:4px 4px 20px 20px}</style></head><body><div class="content"><canvas class="snow"id="snow"></canvas><div class="main-text"><h2>哎呀！<br/>你访问的页面走丢啦！</h1></div><div class="ground"><div class="mound"><div class="mound_text">404</div><div class="mound_spade"></div></div></div></div><script type="text/javascript">(function(){function ready(fn){if (document.readyState!='loading'){fn();}else{document.addEventListener('DOMContentLoaded', fn);}}function makeSnow(el){var ctx=el.getContext('2d');var width=0;var height=0;var particles=[];var Particle=function(){this.x=this.y=this.dx=this.dy=0;this.reset();}
                  Particle.prototype.reset=function(){this.y=Math.random()*height;this.x=Math.random()*width;this.dx=(Math.random()*1)-0.5;this.dy=(Math.random()*0.5)+0.5;}
                  function createParticles(count){if (count!=particles.length) {particles=[];for(var i=0;i<count;i++){particles.push(new Particle());}}}function onResize(){width=window.innerWidth;height=window.innerHeight;el.width=width;el.height=height;createParticles((width*height)/10000);}function updateParticles(){ctx.clearRect(0,0,width,height);ctx.fillStyle='#f6f9fa';particles.forEach(function(particle){particle.y+=particle.dy;particle.x+=particle.dx;if(particle.y>height){particle.y=0;}if(particle.x>width){particle.reset();particle.y=0;}ctx.beginPath();ctx.arc(particle.x,particle.y,5,0,Math.PI*2,false);ctx.fill();});window.requestAnimationFrame(updateParticles);}onResize();updateParticles();window.addEventListener('resize',onResize);}ready(function(){var canvas=document.getElementById('snow');makeSnow(canvas);});})();</script></body></html>
               '''
        
    @app.route('/receivefile')
    def receivefile():
        return '''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>文件上传</title><style> body{padding:0;margin:0;}.file-upload {width: calc(98vw - 12px);padding: 5px;border: 1px solid #999;border-radius: 5px;text-align: center;margin:10px auto;}.button-63 {align-items: center;background-image: linear-gradient(144deg,#AF40FF, #5B42F3 50%,#00DDEB);border: 0;border-radius: 8px;box-shadow: rgba(151, 65, 252, 0.2) 0 15px 30px -5px;box-sizing: border-box;color: #FFFFFF;display: flex;font-family: Phantomsans, sans-serif;font-size: 20px;justify-content: center;line-height: 1em;max-width: 100%;min-width: 140px;padding: 19px 24px;text-decoration: none;user-select: none;-webkit-user-select: none;touch-action: manipulation;white-space: nowrap;cursor: pointer;margin-left: auto;margin-right: auto;}.button-63:active, .button-63:hover {outline: 0;}@media (min-width: 768px) {.button-63 {font-size: 24px;min-width: 196px;}}.file {position: relative;display: inline-block;background: #D0EEFF;border: 1px solid #99D3F5;border-radius: 4px;padding: 4px 12px;overflow: hidden;color: #1E88C7;text-decoration: none;text-indent: 0;line-height: 20px;}.file input {position: absolute;font-size: 100px;right: 0;top: 0;opacity: 0;}.file:hover {background: #AADFFD;border-color: #78C3F3;color: #004974;text-decoration: none;}.progress-bar-container {width: 100%;height: 20px;border: 1px solid #ccc;border-radius: 5px;overflow: hidden;margin-top: 10px;}.progress-bar {height: 100%;width: 0;background-color: #4CAF50;transition: width 0.3s ease-in-out;}.file-list {text-align: left;margin-top: 10px;}ul {list-style-type: none;margin: 0;padding: 0;}li {background-color: #f2f2f2;border: 1px solid #ddd;margin: 10px 0;padding: 10px;height:20px;}li span{float:left;}li button{float:right;}</style></head><body><div class="file-upload"><div id="progressContainer" class="progress-bar-container" style="display: none;"><div id="progressBar" class="progress-bar"></div></div><h1>文件上传</h1><a href="javascript:;" class="file">选择文件<input type="file" id="fileInput" multiple></a><h6>或拖拽文件至此</h6><div class="file-list" id="fileList" style="display: none;"><ul id="fileListItems"></ul></div><button class="button-63" role="button" id="uploadButton" style="display: none;">开始上传</button></div><script>document.getElementById("fileInput").addEventListener("change",function(){var e=document.getElementById("fileList"),t=document.getElementById("fileListItems");if(t.innerHTML="",0===this.files.length)return e.style.display="none",void(document.getElementById("uploadButton").style.display="none");for(var n=0;n<this.files.length;n++){var l=document.createElement("li"),a=document.createElement("span");a.innerText=this.files[n].name;var d=document.createElement("button");d.innerText="×",d.classList.add("button-85"),d.setAttribute("data-index",n),d.addEventListener("click",function(){var e=parseInt(this.getAttribute("data-index")),t=Array.from(document.getElementById("fileInput").files);t.splice(e,1);for(var n=new ClipboardEvent("").clipboardData||new DataTransfer,l=0;l<t.length;l++)n.items.add(t[l]);document.getElementById("fileInput").files=n.files,document.getElementById("fileInput").dispatchEvent(new Event("change"))}),l.appendChild(a),l.appendChild(d),t.appendChild(l)}e.style.display="block",document.getElementById("uploadButton").style.display="block"});var fileUploadArea=document.querySelector(".file-upload");fileUploadArea.addEventListener("dragover",function(e){e.preventDefault(),this.classList.add("dragover")}),fileUploadArea.addEventListener("dragleave",function(){this.classList.remove("dragover")}),fileUploadArea.addEventListener("drop",function(e){e.preventDefault(),this.classList.remove("dragover");var t=e.dataTransfer.files,n=document.getElementById("fileListItems");if(n.innerHTML="",0===t.length)return document.getElementById("fileList").style.display="none",void(document.getElementById("uploadButton").style.display="none");for(var l=0;l<t.length;l++){var a=document.createElement("li"),d=document.createElement("span");d.innerText=t[l].name;var i=document.createElement("button");i.innerText="×",i.classList.add("button-85"),i.setAttribute("data-index",l),i.addEventListener("click",function(){var e=parseInt(this.getAttribute("data-index")),t=Array.from(document.getElementById("fileInput").files);t.splice(e,1);for(var n=new ClipboardEvent("").clipboardData||new DataTransfer,l=0;l<t.length;l++)n.items.add(t[l]);document.getElementById("fileInput").files=n.files,document.getElementById("fileInput").dispatchEvent(new Event("change"))}),a.appendChild(d),a.appendChild(i),n.appendChild(a)}document.getElementById("fileList").style.display="block",document.getElementById("uploadButton").style.display="block",document.getElementById("fileInput").files=t}),document.getElementById("uploadButton").addEventListener("click",function(){this.style.display="none";for(var e=document.getElementsByClassName("button-85"),t=0;t<e.length;t++){e[t].style.display="none"}var n=document.getElementById("fileInput").files;if(0!==n.length){var l=new XMLHttpRequest,a=document.getElementById("progressContainer"),d=document.getElementById("progressBar");l.upload.addEventListener("progress",function(e){var t=e.loaded/e.total*100;d.style.width=t.toFixed(2)+"%"}),l.onreadystatechange=function(){if(l.readyState===XMLHttpRequest.DONE){if(200===l.status){var e=JSON.parse(l.responseText);console.log(e),d.style.width="0%";for(var t="",n=0;n<e.length;n++){if("success"===e[n].status)var i=e[n].filename+'<span style="color:#0f0;">上传成功</span>';else i=e[n].filename+'<span style="color:#f00;">上传失败</span>';t=t+"<li>"+i+"</li>"}}else alert("上传失败");a.style.display="none",fileListItems.innerHTML=t}},a.style.display="block",l.open("POST","/upload",!0);for(var i=new FormData,s=0;s<n.length;s++)i.append("file",n[s]);l.send(i)}else alert("未选择文件")});</script></body></html>'''
    
    @app.route('/list', defaults={'req_path': ''})
    @app.route('/list/<path:req_path>')
    def showlist(req_path):
        abs_path = os.path.join(fol, req_path)

        if not os.path.exists(abs_path):
            abort(404)
            #return "文件不存在", 404

        if os.path.isfile(abs_path):
            global istruerun
            global clients
            global sflj
            istruerun = True 
            sflj = 1 
            client_ip = request.remote_addr
            clients.append(client_ip)
            formatted_time = getnowtime()
            print(Back.WHITE + Fore.GREEN + "\n有新用户接入：{}".format(client_ip) + Style.RESET_ALL, formatted_time)
            print(Fore.YELLOW + "用户{}下载文件：{}".format(client_ip, abs_path) + Style.RESET_ALL)
            return send_from_directory(os.path.dirname(abs_path), os.path.basename(abs_path), as_attachment=True)

        files = os.listdir(abs_path)
        file_list = []

        for file_name in files:
            if file_name in EXCLUDED_DIRS:
                continue 
            try:
                file_path = os.path.join(req_path, file_name)
                abs_file_path = os.path.join(abs_path, file_name)
                mod_datetime = datetime.fromtimestamp(os.path.getmtime(abs_file_path))
                last_modified_time = mod_datetime.strftime("%Y-%m-%d %H:%M")
                            
                if os.path.isdir(abs_file_path):
                    file_list.append({
                        'name': file_name ,
                        'path': file_path,
                        'last_modified': last_modified_time,
                        'type': 'directory'
                    })
                else:
                    size = os.path.getsize(abs_file_path)
                    
                    if size < 1024:
                        size = '%i' % size + ' B'
                    elif 1024 < size <= 1048576:
                        size = '%.1f' % float(size/1024) + ' KB'
                    elif 1048576 < size <= 1073741824:
                        size = '%.1f' % float(size/1048576) + ' MB'
                    elif 1073741824 < size <= 1099511627776:
                        size = '%.1f' % float(size/1073741824) + ' GB'
                        
                    file_list.append({
                        'name': file_name,
                        'path': file_path,
                        'size': size,
                        'last_modified': last_modified_time,
                        'type': 'file'
                    })
            except (PermissionError, FileNotFoundError, OSError) as e:
                print(f"无法获取文件信息 {abs_file_path}: {e}")
                continue
                
        html_content = '''<!DOCTYPE html><html lang="cn"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ShareFile</title><style>body{font-family:Arial,sans-serif;margin:0;padding:5px 20px;background-color:#f4f4f4;color:#333}h2{text-align:center;margin-bottom:0px}.directory-container{display:flex;align-items:center;font-size:18px;margin-bottom:10px}img{margin-right:5px;}.current-path{margin-right:20px}.to-lastPath{background-color:#3498db;color:#fff;border:none;padding:8px 12px;font-size:16px;border-radius:5px;cursor:pointer;margin-left:10px;display:inline-block}.to-lastPath:hover{background-color:#2980b9}.table-container{width:100%;overflow-x:auto}.files-table{width:100%;border-collapse:collapse;margin-top:20px;background-color:#fff;box-shadow:0 4px 8px rgba(0,0,0,.1);min-width:600px}.files-table td,.files-table th{padding:12px 15px;border:1px solid #ddd;text-align:left;white-space:nowrap}.files-table th{background-color:#3498db;color:#fff;text-transform:uppercase;font-size:14px}a{text-decoration:none;color:#3498db;font-weight:700}.files-table td a:hover{text-decoration:none}.files-table td{font-size:16px}@media (max-width:768px){.files-table{min-width:100%}.directory-container{flex-direction:column;align-items:flex-start}}</style></head><body><h2>ShareFile</h2><div class="directory-container"><p class="current-path">当前目录: {% if current_path %}根目录\\{{ current_path }}{% else %} 根目录 {% endif %}</p>{% if current_path %} <button class="to-lastPath" onclick="window.history.back()">返回上级</button> {% endif %}</div><div class="table-container"><table class="files-table"><tr><th class="td-name">名称</th><th class="td-size">大小</th><th class="td-ctime">修改日期</th></tr>{% for file in files %}<tr><td data-label="名称"><a href="{{ url_for('showlist', req_path=file.path) }}">{% if file.type == 'file' %}<img src="data:image/gif;base64,R0lGODlhEAAQALMAAAAAAIAAAACAAICAAAAAgIAAgACAgMDAwICAgP8AAAD/AP//AAAA//8A/wD//////yH5BAEAAA0ALAAAAAAQABAAAAQwsDVEq5V4vs03zVrHIQ+SkaJXYWg6sm5nSm08h3EJ5zrN9zjbLneruYo/JK9oaa4iADs="/>{% else %}<img src="data:image/gif;base64,R0lGODlhEAAQALMAAJF7Cf8A//zOLQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAAAEALAAAAAAQABAAAAQqMMhJqwQ42wmE/8AWdB+YaWSZqmdWsm9syjJGx/YN6zPv5T4gr0UkikQRADs="/>{% endif %}{{ file.name }}</a></td><td data-label="大小">{% if file.size %} <span>{{ file.size }}</span> {% else %}  {% endif %}</td><td data-label="修改日期">{{ file.last_modified }}</td></tr>{% endfor %}</table></div></body></html>'''
        file_list = sorted(file_list, key=lambda x: (x['type'] == 'file', x['name'].lower()))
        return render_template_string(html_content, files=file_list, current_path=req_path)
    
    @app.route('/upload', methods=['POST'])
    def upload():
        global istruerun
        global clients
        global sflj
        istruerun = True 
        sflj = 1 
        client_ip = request.remote_addr
        clients.append(client_ip)
        formatted_time = getnowtime()
        
        print(Back.WHITE + Fore.GREEN + "\n有新用户接入：{}".format(client_ip) + Style.RESET_ALL, formatted_time)
        if 'file' not in request.files:
            return jsonify({'error': 'No file selected'})
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        files = request.files.getlist('file')
        filelist = []
        for file in files:
            filelist.append(file.filename)
        print(Fore.YELLOW + "\n用户{}上传文件：{}".format(client_ip, filelist) + Style.RESET_ALL)
        responses = []
        for file in files:
            filename = file.filename
            while os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
                name, ext = os.path.splitext(filename)
                now = datetime.now()
                filename = name + '_' + now.strftime("%Y%m%d%H%M%S") + ext
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            responses.append({'filename': filename, 'status': 'success'})
        return jsonify(responses)

    @app.route('/download/<filename>', methods=['GET'])
    def download_file(filename):
        global istruerun
        global clients
        global sflj
        istruerun = True 
        sflj = 1 
        client_ip = request.remote_addr
        clients.append(client_ip)
        formatted_time = getnowtime()
        print(Back.WHITE + Fore.GREEN + "\n有新用户接入：{}".format(client_ip) + Style.RESET_ALL, formatted_time)
        file_path = os.path.join(fol, filename)
        if not os.path.exists(file_path):
            #return "文件不存在", 404
            abort(404)
        print(Fore.YELLOW + "用户{}下载文件：{}".format(client_ip, file_path) + Style.RESET_ALL)
        return send_from_directory(fol, filename, as_attachment=True, conditional=True)
         
    app.run(host=cip, port=p, debug=False, threaded=True)

def getnowtime():
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_time

def get_sendto_directory():
    try:
        sendto_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders")
        sendto_directory, _ = winreg.QueryValueEx(sendto_key, "SendTo")
        return sendto_directory
    except Exception as e:
        print(f"Error occurred while getting 'SendTo' directory: {str(e)}")
        return None

def set_shortcut():
    sendto_dir = get_sendto_directory()
    args = sys.argv
    executable_path = os.path.abspath(sys.executable)
    if getattr(sys, 'frozen', False):
        exe = executable_path
        arguments = None
    else:
        exe = executable_path 
        arguments = args[0]
    lnkname = sendto_dir + r"\打包分享.lnk"
    try:
        shortcut = pythoncom.CoCreateInstance(
            CLSID_ShellLink, None,
            pythoncom.CLSCTX_INPROC_SERVER, IID_IShellLink)
        shortcut.SetPath(exe)
        if arguments:
            shortcut.SetArguments(arguments)
        if not lnkname.endswith('.lnk'):
            lnkname += ".lnk"
        shortcut.QueryInterface(pythoncom.IID_IPersistFile).Save(lnkname, 0)
        return True
    except Exception as e:
        print(e.args)
        return False

def get_active_network_interfaces(): #获取活动网卡的连接名和IP地址
    active_interfaces = []
    interfaces = psutil.net_if_stats()
    for interface_name, interface in interfaces.items():
        if interface.isup:
            interface_addresses = psutil.net_if_addrs().get(interface_name)
            if interface_addresses:
                for address in interface_addresses:
                    if address.family == socket.AF_INET:  # 只处理 IPv4 地址
                        if address.address != '127.0.0.1':  # 排除回环地址
                            active_interface = {
                                'name': interface_name,
                                'ip_address': address.address
                            }
                            active_interfaces.append(active_interface)
                            break  # 如果有一个活动地址，就认为该网卡是活动的
    return active_interfaces

def get_all_ips(): #获取本机所有IP地址（废弃）
    interfaces = netifaces.interfaces()
    ip_addresses = []
    for interface in interfaces:
        addresses = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in addresses:
            for address in addresses[netifaces.AF_INET]:
                ip_address = address['addr']
                if ip_address != '127.0.0.1':
                    ip_addresses.append(ip_address)
    return ip_addresses
    
def get_ip_address_by_interface_name(interface_name): #根据连接名获取IP地址
    interfaces = psutil.net_if_addrs()
    for interface in interfaces.get(interface_name, []):
        if interface.family == socket.AF_INET:  # 只处理IPv4地址
            ip_address = interface.address
            return ip_address
    return None
    
def input_port():
    while True:
        pp = input("请输入要使用的端口（建议10000~65535），按回车确认；或直接回车使用随机端口：")
        if not pp:
            print("使用随机端口")
            return 0
        try:
            p = int(pp)
            if 1 <= p <= 65535:
                print(f"使用端口：{p}")
                return p
        except:
            pass

def choose_ip():  # 选择要使用的网络接口(多选)
    all_ips = get_active_network_interfaces()
    active_interface = {'name': '所有网络接口', 'ip_address': '0.0.0.0'}
    all_ips.append(active_interface)

    ip_count = len(all_ips)
    for i, interface in enumerate(all_ips):
        print(Fore.CYAN + f"{i + 1}、{interface['name']}（{interface['ip_address']}）" + Style.RESET_ALL)

    selected_ips = []  # 存储用户选择的网络接口
    while True:
        selected_index = input("选择要使用的网络接口，并输入编号，多个编号用英文逗号分隔，按回车确认：")
        selected_indices = selected_index.split(',')  # 以逗号分隔多个编号
        try:
            selected_indices = [int(index) for index in selected_indices]
            if all(1 <= index <= ip_count for index in selected_indices):  # 检查编号是否有效
                selected_ips = [all_ips[index - 1] for index in selected_indices]  # 获取用户选择的网络接口
                print(Fore.GREEN + "已选择网络接口：" + ", ".join(f"{interface['name']}（{interface['ip_address']}）" for interface in selected_ips) + Style.RESET_ALL)
                return [interface['name'] for interface in selected_ips]  # 返回选择的网络接口名称列表
            else:
                print(Back.RED + Fore.WHITE + "无效的编号，请重新输入！" + Style.RESET_ALL)
        except ValueError:
            print(Back.RED + Fore.WHITE + "无效的编号，请重新输入！" + Style.RESET_ALL)
    
    
def choose_ip_onlyone(): #选择要使用的网络接口（废弃）
    all_ips = get_active_network_interfaces()
    active_interface = {'name': '所有网络接口','ip_address': '0.0.0.0'}
    all_ips.append(active_interface)
    
    ip_count = len(all_ips)
    for i, interface in enumerate(all_ips):
        print(Fore.CYAN + f"{i+1}、{interface['name']}（{interface['ip_address']}）" + Style.RESET_ALL)
    while True:
        selected_index = input("选择要使用的网络接口，并输入编号，按回车确认：")
        try:
            selected_index = int(selected_index)  
            if selected_index >= 1 and selected_index <= ip_count:
                selected_ip = all_ips[selected_index - 1]
                print(Fore.GREEN + f"已选择网络接口：{selected_ip['name']}（{selected_ip['ip_address']}）" + Style.RESET_ALL)
                return selected_ip['name']
            else:
                print(Back.RED + Fore.WHITE + "无效的编号，请重新输入！" + Style.RESET_ALL)
        except ValueError:
            print(Back.RED + Fore.WHITE + "无效的编号，请重新输入！" + Style.RESET_ALL)
           
def write_registry_entry(epath, ico, cip, port): #将配置信息写入注册表
    entries = [
        (r"*\shell\Share File", "分享此文件", epath + ' S "%1"'),
        (r"Directory\shell\Share File", "打包分享此文件夹", epath + ' S "%1"'),
        (r"Directory\shell\Share List", "列表分享此文件夹", epath + ' F "%1"'),
        (r"Directory\shell\Receive File", "接收文件至此目录", epath + ' R "%1"'),
        (r"Drive\shell\Receive File", "接收文件至此磁盘", epath + ' R "%1"'),
        (r"Drive\shell\Share List", "列表分享此磁盘", epath + ' F "%1"'),
        (r"Directory\Background\shell\Receive File", "接收文件至此目录", epath + ' R "%v"'),
        (r"Directory\Background\shell\Share List", "列表分享此目录", epath + ' F "%v"')
    ]
    for reg_path, name, command in entries:
        key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, reg_path)
        winreg.SetValue(key, None, winreg.REG_SZ, name)
        winreg.SetValueEx(key, 'ICON', 0, winreg.REG_SZ, ico)
        winreg.SetValueEx(key, 'ip', 0, winreg.REG_SZ, cip)
        winreg.SetValueEx(key, 'autoexit', 0, winreg.REG_SZ, "0")
        winreg.SetValueEx(key, 'showqr', 0, winreg.REG_SZ, "1")
        winreg.SetValueEx(key, 'port', 0, winreg.REG_SZ, str(port))
        winreg.CloseKey(key)
        
        command_path = reg_path + r"\command"
        command_key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, command_path)
        winreg.SetValue(command_key, None, winreg.REG_SZ, command)
        winreg.CloseKey(command_key)

def write_registry_entry_old(epath, ico,cip): #写入注册表(废弃，替换为上面的函数)
    reg_path = r"*\shell\Share File"
    key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, reg_path)
    winreg.SetValue(key, None, winreg.REG_SZ, "分享此文件")
    winreg.SetValueEx(key, 'ICON', 0, winreg.REG_SZ, ico)
    winreg.SetValueEx(key, 'ip', 0, winreg.REG_SZ, cip)
    winreg.SetValueEx(key, 'autoexit', 0, winreg.REG_SZ, "1")
    winreg.SetValueEx(key, 'showqr', 0, winreg.REG_SZ, "1")
    winreg.CloseKey(key)

    command_path = r"*\shell\Share File\command"
    command_key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, command_path)
    winreg.SetValue(command_key, None, winreg.REG_SZ, epath + ' S "%1"')
    winreg.CloseKey(command_key)
    
    reg_path = r"Directory\shell\Share File"
    key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, reg_path)
    winreg.SetValue(key, None, winreg.REG_SZ, "打包分享此文件夹")
    winreg.SetValueEx(key, 'ICON', 0, winreg.REG_SZ, ico)
    winreg.CloseKey(key)

    command_path = r"Directory\shell\Share File\command"
    command_key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, command_path)
    winreg.SetValue(command_key, None, winreg.REG_SZ, epath + ' S "%1"')
    winreg.CloseKey(command_key)
    
    reg_path = r"Folder\shell\Receive File"
    key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, reg_path)
    winreg.SetValue(key, None, winreg.REG_SZ, "接收文件至此目录")
    winreg.SetValueEx(key, 'ICON', 0, winreg.REG_SZ, ico)
    winreg.CloseKey(key)

    command_path = r"Folder\shell\Receive File\command"
    command_key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, command_path)
    winreg.SetValue(command_key, None, winreg.REG_SZ, epath + ' R "%1"')
    winreg.CloseKey(command_key)
    
    reg_path = r"Directory\Background\shell\Receive File"
    key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, reg_path)
    winreg.SetValue(key, None, winreg.REG_SZ, "接收文件至此目录")
    winreg.SetValueEx(key, 'ICON', 0, winreg.REG_SZ, ico)
    winreg.CloseKey(key)

    command_path = r"Directory\Background\shell\Receive File\command"
    command_key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, command_path)
    winreg.SetValue(command_key, None, winreg.REG_SZ, epath + ' R "%v"')
    winreg.CloseKey(command_key)

def read_registry_value(): #读取注册表中PY文件的默认打开程序（此函数已废弃）
    try:
        key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, r"Python.File\Shell\open\command")
        value, _ = winreg.QueryValueEx(key, "")
        winreg.CloseKey(key)
        value = value.split('"')
        return value[1]
    except OSError:
        print("注册表项不存在")
    except Exception as e:
        print(f"读取注册表值时出现错误: {e}")

def check_reg_key(keyname): #读取注册表HKCR下的指定项
    key_path = r'*\shell\Share File'
    try:
        key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, key_path)
        value, reg_type = winreg.QueryValueEx(key, keyname)
        return value
    except FileNotFoundError:
        return None

def CheckPortUse(port): #检测端口是否被占用
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    if result == 0:
        sock.close()
        return False
    else:
        connections = psutil.net_connections()
        for conn in connections:
            if conn.laddr.port == port:
                return False
        return True

def get_port_connections(port): #获取本机端口的连接状态
    global sflj
    global clients
    global old_ips
    formatted_time = getnowtime()
    connections = psutil.net_connections()
    ips = []
    for conn in connections:
        if conn.laddr.port == port:
            if conn.status == 'ESTABLISHED':
                ips.append(conn.raddr.ip)
                
    diff2 = set(clients).difference(set(ips))
    if diff2:
        print(Back.RED + Fore.WHITE + "\n用户：{}已断开连接。".format(list(diff2)) + Style.RESET_ALL, formatted_time)
    clients = list(set(clients).difference(diff2))
    
    ipnum = len(list(set(ips)))
    if ipnum > 0:
        if sflj == 0:
            sflj += 1
        if ips != old_ips:
            old_ips = ips
            print(Fore.GREEN + "\n在线用户：{}".format(list(set(ips))) + Style.RESET_ALL, formatted_time, end="")
        else:
            print(Fore.GREEN + "\r在线用户：{}".format(list(set(ips))) + Style.RESET_ALL, formatted_time, end="")
        return False
    else:
        if sflj == 0:
            #print("暂无用户连接")
            return False
        else:
            #print("所有用户都断开连接")
            return True

def extract_domain_or_ip(url):
    if url.startswith("http://"):
        url = url[7:]
    elif url.startswith("https://"):
        url = url[8:]
    if "/" in url:
        url = url[:url.index("/")]
    if ":" in url:
        url = url[:url.index(":")]
    return url
            
def save_qr_code(img, index): #保存二维码图片
    filename = filedialog.asksaveasfilename(defaultextension=".png",
                                            filetypes=[("PNG Image", "*.png")],
                                            initialfile="文件分享二维码.png")
    if filename:
        img.save(filename)

def show_qr_code(data_list): #生成并显示二维码
    qr_count = len(data_list)
    max_width = 200
    max_height = 200
    window_width = (max_width + 15) * qr_count
    window_height = max_height + 60
    window = tk.Tk()
    window.title("二维码分享")
    window.geometry(f"{window_width}x{window_height}")
    window.resizable(False, False)
    window.attributes('-toolwindow', True)
    for i, data in enumerate(data_list):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=3,
        )
        qr.add_data(data, optimize=0)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        width, height = img.size
        
        if width > max_width or height > max_height:
            scale = min(max_width/width, max_height/height)
            new_width = int(width * scale)
            new_height = int(height * scale)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
        # 在二维码上添加文字
        text = extract_domain_or_ip(data)
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()  # 使用系统默认字体
        text_bbox = draw.textbbox((0, 0), text, font=font)  # 获取文字的边界框
        text_position = ((new_width - text_bbox[2]) // 2, new_height - 12)  # 调整文字的垂直位置
        draw.text(text_position, text, fill="black", font=font)  # 使用变量text中的内容
            
        photo = ImageTk.PhotoImage(img)
        label = tk.Label(window, image=photo)
        label.image = photo  # 保持对图像的引用，避免被垃圾回收
        label.grid(row=0, column=i, padx=5, pady=5)
        save_button = tk.Button(window, text=f"保存二维码 {i+1}", command=lambda img=img, index=i+1: save_qr_code(img, index))
        save_button.grid(row=1, column=i, padx=5, pady=5)
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    x = int((screen_width - window_width) / 2)
    y = int((screen_height - window_height) / 2)
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    window.mainloop()

def sys_init(arg):
    #ip = cip = choose_ip()
    iplist = choose_ip()
    if '所有网络接口' in iplist:
        iplist = ["所有网络接口"]
    port = input_port()
    executable_path = os.path.abspath(sys.executable)
    if getattr(sys, 'frozen', False):
        exe = icon = '"' + executable_path + '"'
        #print("脚本已编译成exe文件")
    else:
        #pypath = read_registry_value() #从注册表中读取.py文件的默认打开程序
        exe = '"' + executable_path + '" "' + arg[0] + '"'
        icon = '"' + executable_path + '"'
        #print("脚本未被编译成exe文件")
    write_registry_entry(exe, icon, str(iplist), port)
    set_shortcut()
    return iplist, port 

def qr_code_thread(url):
    show_qr_code(url)

def user_colse(tempfile):
    print("\n程序将退出")
    time.sleep(3)
    if os.path.exists(tempfile):
        os.remove(tempfile)
    os._exit(0)

def zip_files(paths, zipfilename):
    print("打包中，请稍后")
    with zipfile.ZipFile(zipfilename, 'w', zipfile.ZIP_STORED) as zipf:
        for path in paths:
            if os.path.isdir(path):
                dir_name = os.path.basename(path)
                files = []
                for root, directories, filenames in os.walk(path):
                    for filename in filenames:
                        files.append(os.path.join(root, filename))
                zipf.write(path, arcname=dir_name)
                for file in files:
                    arcname = os.path.join(dir_name, os.path.relpath(file, path))
                    zipf.write(file, arcname=arcname)
            elif os.path.isfile(path):
                zipf.write(path, arcname=os.path.basename(path))
    os.system("cls" if os.name in ("nt", "dos") else "clear") #清除控制台内容

def zip_folder(folder_path): #废弃
    temp_dir = tempfile.gettempdir()
    folder_name = os.path.basename(folder_path)
    zip_file_path = os.path.join(temp_dir, folder_name + '.zip')
    try:
        with zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_STORED) as zipf:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, folder_path)
                    zipf.write(file_path, arcname=arcname)
        return zip_file_path
    except:
        return "ERR"
        
def uninstall_app():#卸载，删除添加的右键菜单和创建的快捷方式
    reg_paths = [
        r"*\shell\Share File",
        r"Directory\shell\Share File",
        r"Directory\shell\Share List",
        r"Directory\shell\Receive File",
        r"Drive\shell\Receive File",
        r"Drive\shell\Share List",
        r"Directory\Background\shell\Receive File",
        r"Directory\Background\shell\Share List"
    ]
    for reg_path in reg_paths:
        try:
            command_path = reg_path + "\\command"
            winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, command_path)
        except WindowsError:
            pass
        try:
            winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, reg_path)
        except WindowsError:
            pass
    sendto_dir = get_sendto_directory()
    lnkname = sendto_dir + r"\打包分享.lnk"
    if os.path.exists(lnkname):
        os.remove(lnkname)
    print("卸载完成")
    time.sleep(3)
    
def show_info(ip, port, path, filename, ips):
    qrcode_data = []
    if isinstance(ip, str):
        url = "http://" + ip + ":" + str(port) + "/download/" + filename
        pyperclip.copy(url)
        qrcode_data.append(url)
        print(Back.BLUE + Fore.WHITE + "\n↓↓文件下载地址已复制到剪贴板↓↓\n" + Style.RESET_ALL)
        print(Back.GREEN + Fore.WHITE + url + Style.RESET_ALL)
        print(Back.BLUE + Fore.WHITE + "\n↑↑文件下载地址已复制到剪贴板↑↑\n" + Style.RESET_ALL)
    elif isinstance(ip, list):
        print(Back.BLUE + Fore.WHITE + "\n↓↓文件下载地址↓↓\n" + Style.RESET_ALL)
        for index, pp in enumerate(ip):
            url = "http://" + pp + ":" + str(port) + "/download/" + filename
            pyperclip.copy(url)
            qrcode_data.append(url)
            print("网络接口" + str(index + 1) + "（" + ips[index]['name'] + "）：" + Back.GREEN + Fore.WHITE + url + Style.RESET_ALL)
            print("\n")
        print(Back.BLUE + Fore.WHITE + "↑↑文件下载地址（最后一条已复制到剪贴板）↑↑\n" + Style.RESET_ALL)
    return qrcode_data
            
if __name__ == '__main__':
    init(autoreset=True) #背景色
    os.system("cls" if os.name in ("nt", "dos") else "clear") #清除控制台内容
    args = sys.argv #获取参数
    interface_name = check_reg_key("ip") #从注册表中获取设置的网络接口信息
    port = check_reg_key("port")
    if interface_name == None: #如未设置网络接口，认为程序程序首次运行
        arguments = sys_init(args) #程序首次运行，进行初始化操作
        interface_name = arguments[0]
        port = arguments[1]
    else:
        interface_name = eval(interface_name)
    
    if len(args) == 1: #如果只有一个参数
        print(Back.RED + Fore.WHITE + "\n**请通过右键菜单运行此程序**\n" + Style.RESET_ALL)
        #print(Back.BLUE + Fore.WHITE + "Tips:如不需自动退出和二维码功能，请在注册表HKEY_CLASSES_ROOT\\*\\shell\\Share File中自行修改" + Style.RESET_ALL)
        hc = input("\n直接按回车键退出程序；输入“0”按回车卸载程序；输入其他内容按回车重新设置网络接口：")
        if hc != "":
            if str(hc) == "0":
                uninstall_app() #卸载程序设置的右键菜单
            else:
                sys_init(args) #重新初始化程序
        sys.exit(0)
        
    if str(port) == "0":
        while True: #随机生成一个系统未占用的端口
            port = random.randint(10000, 65500)
            if CheckPortUse(port):
                break
    else:
        port = int(port)
            
    flask_ip = "0.0.0.0"   
    ip_s = get_active_network_interfaces() #获取所有网卡IP地址，放入列表中  
    ip = []  
    ips = []    
    if '所有网络接口' in interface_name:
        for a in ip_s:
            ip.append(a['ip_address']) 
        ips = ip_s 
    else:
        for a in ip_s:
            if a['name'] in interface_name:
                ip.append(a['ip_address']) 
                ips.append(a)

    zip_file = "" #
    
    if args[1] == "S": #发送文件参数
        file = args[2] #从参数中取待发送文件（夹）具体路径
        if os.path.isdir(file): #如果待发送的是文件夹
            temp_dir = tempfile.gettempdir() #获取系统临时目录
            folder_name = os.path.basename(file) #获取待发送文件夹名称
            zip_file = os.path.join(temp_dir, folder_name + '.zip') #拼接文件夹压缩后的zip文件路径
            d = []
            d.append(file) #
            #file = zip_file = zip_folder(file)
            zip_files(d, zip_file) #压缩文件夹
            file = zip_file
        elif os.path.isfile(file):
            pass
        path = os.path.dirname(file) #
        filename = os.path.basename(file) #
        
        qrcode_data = show_info(ip, port, path, filename, ips) #显示下载地址，并返回下载地址待生成二维码
    elif args[1] == "R": #接收文件
        qrcode_data = []
        path = args[2]
        path = path.strip('"')
        if not path.endswith(os.path.sep):
            path += os.path.sep
        if isinstance(ip, str):
            url = "http://" + ip + ":" + str(port) + "/receivefile"
            pyperclip.copy(url)
            qrcode_data.append(url)
            print(Back.BLUE + Fore.WHITE + "\n↓↓文件上传地址已复制到剪贴板↓↓\n" + Style.RESET_ALL)
            print(Back.GREEN + Fore.WHITE + url + Style.RESET_ALL)
            print(Back.BLUE + Fore.WHITE + "\n↑↑文件上传地址已复制到剪贴板↑↑\n" + Style.RESET_ALL)
        elif isinstance(ip, list):
            print(Back.BLUE + Fore.WHITE + "\n↓↓文件上传地址↓↓\n" + Style.RESET_ALL)
            for index, pp in enumerate(ip):
                url = "http://" + pp + ":" + str(port) + "/receivefile"
                pyperclip.copy(url)
                qrcode_data.append(url)
                print("网络接口" + str(index + 1) + "（" + ips[index]['name'] + "）：" + Back.GREEN + Fore.WHITE + url + Style.RESET_ALL)
                print("\n")
            print(Back.BLUE + Fore.WHITE + "↑↑文件上传地址（最后一条已复制到剪贴板）↑↑\n" + Style.RESET_ALL)
    elif args[1] == "F":   #列表分享文件
        qrcode_data = []
        path = args[2]
        path = path.strip('"')
        if not path.endswith(os.path.sep):
            path += os.path.sep
        if isinstance(ip, str):
            url = "http://" + ip + ":" + str(port) + "/list"
            pyperclip.copy(url)
            qrcode_data.append(url)
            print(Back.BLUE + Fore.WHITE + "\n↓↓文件分享地址已复制到剪贴板↓↓\n" + Style.RESET_ALL)
            print(Back.GREEN + Fore.WHITE + url + Style.RESET_ALL)
            print(Back.BLUE + Fore.WHITE + "\n↑↑文件分享地址已复制到剪贴板↑↑\n" + Style.RESET_ALL)
        elif isinstance(ip, list):
            print(Back.BLUE + Fore.WHITE + "\n↓↓文件分享地址↓↓\n" + Style.RESET_ALL)
            for index, pp in enumerate(ip):
                url = "http://" + pp + ":" + str(port) + "/list"
                pyperclip.copy(url)
                qrcode_data.append(url)
                print("网络接口" + str(index + 1) + "（" + ips[index]['name'] + "）：" + Back.GREEN + Fore.WHITE + url + Style.RESET_ALL)
                print("\n")
            print(Back.BLUE + Fore.WHITE + "↑↑文件分享地址（最后一条已复制到剪贴板）↑↑\n" + Style.RESET_ALL)
        
    else:
        arguments = sys.argv[1:]
        
        temp_dir = tempfile.gettempdir()
        now = datetime.now()
        filename = now.strftime("%Y%m%d%H%M%S")
        zip_file = os.path.join(temp_dir, filename + '.zip')
        zip_files(arguments, zip_file)
        
        path = os.path.dirname(zip_file)
        filename = os.path.basename(zip_file)
        
        qrcode_data = show_info(ip, port, path, filename, ips)
    
    print("Tips：如无法重新复制上方链接，可在此窗口标题栏点击右键选择属性，勾选“快速编辑模式”，点击确定保存。")
    print(Fore.GREEN + "\n 文登信息中心 \n" + Style.RESET_ALL)

    qr = check_reg_key("showqr")
    if str(qr) == "1":
        print(Back.CYAN + Fore.WHITE + "显示二维码：" + Style.RESET_ALL, Back.GREEN + Fore.WHITE + " 开 " + Style.RESET_ALL)
        print(Fore.YELLOW + "如不需二维码功能请在注册表HKEY_CLASSES_ROOT\\*\\shell\\Share File\\showqr中自行修改值为0"+ Style.RESET_ALL)
        qr_thread = threading.Thread(target=qr_code_thread, args=(qrcode_data,))
        qr_thread.start()
    else:
        print(Back.CYAN + Fore.WHITE + "显示二维码：" + Style.RESET_ALL, Back.RED + Fore.WHITE + " 关 " + Style.RESET_ALL)
        print(Fore.YELLOW + "如需开启二维码功能请在注册表HKEY_CLASSES_ROOT\\*\\shell\\Share File\\showqr中自行修改值为1"+ Style.RESET_ALL)

    autoexit = check_reg_key("autoexit")
    if str(autoexit) == "1":
        print(Back.CYAN + Fore.WHITE + "所有连接关闭将自动退出功能：" + Style.RESET_ALL,  Back.GREEN + Fore.WHITE + " 开 " + Style.RESET_ALL)
        print(Fore.YELLOW + "如不需自动退出功能请在注册表HKEY_CLASSES_ROOT\\*\\shell\\Share File\\autoexit中自行修改值为0"+ Style.RESET_ALL)
    else:
        print(Back.CYAN + Fore.WHITE + "所有连接关闭将自动退出功能：" + Style.RESET_ALL,  Back.RED + Fore.WHITE + " 关 " + Style.RESET_ALL)
        print(Fore.YELLOW + "如需开启自动退出功能请在注册表HKEY_CLASSES_ROOT\\*\\shell\\Share File\\autoexit中自行修改值为1"+ Style.RESET_ALL)

    columns = shutil.get_terminal_size().columns
    print('~' * columns)
    
    server_thread = threading.Thread(target=start_flask_server, args=(port, path, flask_ip))
    server_thread.start()
    
    sflj = 0 #用于判断是否有用户连接过，当连接用户数为0，通过此参数判断是从未有用户连接过还是所有用户均已断开连接
    clients = [] #记录在线用户IP组
    istruerun = False #判断用户是否真的发生上传下载事件
    old_ips = [] #貌似跟变量clients一个作用，但懒得修改了
    try:
        while True:
            zt = get_port_connections(port)
            if istruerun and zt and str(autoexit) == "1":
                user_colse(zip_file)
            time.sleep(3)
    except KeyboardInterrupt:
        user_colse(zip_file)
    except SystemExit:
        user_colse(zip_file)
        
