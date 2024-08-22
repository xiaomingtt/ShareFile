# -*- coding: utf-8 -*-

from flask import Flask, send_from_directory, request, jsonify #Flask==3.0.0
import os
import sys
import random
import pyperclip                                               #pyperclip==1.8.2
import winreg
import socket
import psutil                                                  #psutil==5.9.6
import time
import threading 
import tkinter as tk 
from tkinter import filedialog
from PIL import ImageTk, Image, ImageDraw, ImageFont           #Pillow==9.2.0
import qrcode                                                  #qrcode==7.4.2
from colorama import init, Fore, Back, Style                   #colorama==0.4.6
from datetime import datetime
import shutil
import logging
import zipfile
import tempfile
import pythoncom                                               #pywin32==300
from win32com.shell import shell, shellcon

CLSID_ShellLink = shell.CLSID_ShellLink
IID_IShellLink = shell.IID_IShellLink

def start_flask_server(p, fol, cip):
    app = Flask(__name__)
    app.config["UPLOAD_FOLDER"] = fol
    app.config["UPLOAD_TEMP_FOLDER"] = fol
    app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024 * 1024
    
    logging.getLogger("werkzeug").disabled = True
    
    @app.before_request
    def check_auth():
        client_ip = request.remote_addr

    @app.route('/')
    def index():
        html1 = '''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport"content="width=device-width, initial-scale=1.0"><title>局域网文件传输助手</title><style type="text/css">#mine{margin:5px auto}.level{text-align:center;margin-bottom:10px}.level button{padding:5px 15px;background-color:#02a4ad;border:none;color:#fff;border-radius:3px;outline:none;cursor:pointer}.level button.active{background-color:#00abff}table{border-spacing:1px;background-color:#929196;margin:0 auto}td{padding:0;width:20px;height:20px;background-color:#ccc;border:2px solid;border-color:#fff#a1a1a1#a1a1a1#fff;text-align:center;line-height:20px;font-weight:bold}.tips{color:red;font-size:16px}.mine{background:#d9d9d9 url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAARFJREFUOE+V0r1KA0EUxfHf7orgGwhKEAIW0cbCRhsLSz8qLXwFX0CwsRJfw8IqhWgvpvABbGIloiDWdjaZXY1uYLPZZON0M3Pvf+aecyLDq4WnmLOYTo9O6X5kG1UU/EISdjJWUy4mQcqAVsxByiVe617v31f9oNi3HHOUF3YD7TJ0EmA+4Rbrg6YfwEp/vCKkEhBzEnGM50LxV0Yj5bAIGQEk7OFm3PwZ3SKkCvCAzUkCZpymnFeJ2Eh4m0L9u8D2CGCGrYz7KQBC7mB5hNmET8zVQF4Czcoc5Nbt1gDa4c+NyiA1k2H7yqyPwMLgcFyQlhKusFHsznhMWasNUl7Q12M/YxG9iPfA9X+iPI0ZvgGuQTgRPscqngAAAABJRU5ErkJggg==)no-repeat center;background-size:cover}.flag{background:#ccc url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAALxJREFUOE/tkyEOAjEQRd/4JQFFglrFCfDsLQgCwU3gGmDQCCyGhDUcgVWrOQCshAx0KUmztKE4BDUV8+d1Mr9fsEdprUELkCGQAUegAN0J1eKla97iAPa20ac9gS5toQ8yBp0L1SwW4IH+AZ+WaCzsAZ2QfQGAbICtcC5No5KMQCbAAOg6sNwC8oaNtTW571WlncI1NTVXEw2I/InhCX4coCTZI4UmTCvhMg1b916pl/jc8O1gEmcS9g3gDoHKYhEZ0qyeAAAAAElFTkSuQmCC)no-repeat center;background-size:cover}.info{margin-top:10px;text-align:center}td.zero{background-color:#d9d9d9;border-color:#d9d9d9}td.one{background-color:#d9d9d9;border-color:#d9d9d9;color:#0332fe}td.two{background-color:#d9d9d9;border-color:#d9d9d9;color:#019f02}td.three{background-color:#d9d9d9;border-color:#d9d9d9;color:#ff2600}td.four{background-color:#d9d9d9;border-color:#d9d9d9;color:#93208f}td.five{background-color:#d9d9d9;border-color:#d9d9d9;color:#ff7f29}td.six{background-color:#d9d9d9;border-color:#d9d9d9;color:#ff3fff}td.seven{background-color:#d9d9d9;border-color:#d9d9d9;color:#3fffbf}td.eight{background-color:#d9d9d9;border-color:#d9d9d9;color:#22ee0f}.titl{width:100%;text-align:center;font-size:20px;color:#1296db;margin-bottom:10px}</style></head><body><div id="mine"><div class="titl">欢迎使用局域网文件传输助手<br>放松一下吧</div><div class="level"><button class="active">初级</button><button>中级</button><button>高级</button><button>重新开始</button></div><div class="gameBox"></div><div class="info">剩余雷数：<span class="mineNum"></span><br><span class="tips">左键扫雷，右键插旗，再次点击右键拔旗</span></div></div><script type="text/javascript">function Mine(t,e,s){this.tr=t,this.td=e,this.mineNum=s,this.squares=[],this.tds=[],this.surplusMine=s,this.allRight=!1,this.parent=document.querySelector(".gameBox")}Mine.prototype.randomNum=function(){for(var t=new Array(this.tr*this.td),e=0;e<t.length;e++)t[e]=e;return t.sort(function(){return.5-Math.random()}),t.slice(0,this.mineNum)},Mine.prototype.init=function(){for(var t=this.randomNum(),e=-1,s=0;s<this.tr;s++){this.squares[s]=[];for(var i=0;i<this.td;i++)e++,-1!=t.indexOf(e)?this.squares[s][i]={type:"mine",x:i,y:s}:this.squares[s][i]={type:"number",x:i,y:s,value:0}}this.updateNum(),this.createDom(),this.parent.oncontextmenu=function(){return!1},this.mineNumDom=document.querySelector(".mineNum"),this.mineNumDom.innerHTML=this.surplusMine},Mine.prototype.createDom=function(){for(var t=this,e=document.createElement("table"),s=0;s<this.tr;s++){var i=document.createElement("tr");this.tds[s]=[];for(var n=0;n<this.td;n++){var r=document.createElement("td");this.tds[s][n]=r,r.pos=[s,n],r.onmousedown=function(){t.play(event,this)},i.appendChild(r)}e.appendChild(i)}this.parent.innerHTML="",this.parent.appendChild(e)},Mine.prototype.getAround=function(t){for(var e=t.x,s=t.y,i=[],n=e-1;n<=e+1;n++)for(var r=s-1;r<=s+1;r++)n<0||r<0||n>this.td-1||r>this.tr-1||n==e&&r==s||"mine"==this.squares[r][n].type||i.push([r,n]);return i},Mine.prototype.updateNum=function(){for(var t=0;t<this.tr;t++)for(var e=0;e<this.td;e++)if("number"!=this.squares[t][e].type)for(var s=this.getAround(this.squares[t][e]),i=0;i<s.length;i++)this.squares[s[i][0]][s[i][1]].value+=1},Mine.prototype.play=function(t,e){var s=this;if(1==t.which&&"flag"!=e.className){var n=this.squares[e.pos[0]][e.pos[1]],r=["zero","one","two","three","four","five","six","seven","eight"];if("number"==n.type){if(e.innerHTML=n.value,e.className=r[n.value],0==n.value){e.innerHTML="",function t(e){for(var i=s.getAround(e),n=0;n<i.length;n++){var a=i[n][0],o=i[n][1];s.tds[a][o].className=r[s.squares[a][o].value],0==s.squares[a][o].value?s.tds[a][o].check||(s.tds[a][o].check=!0,t(s.squares[a][o])):s.tds[a][o].innerHTML=s.squares[a][o].value}}(n)}}else this.gameOver(e)}if(3==t.which){if(e.className&&"flag"!=e.className)return;if(e.className="flag"==e.className?"":"flag","mine"==this.squares[e.pos[0]][e.pos[1]].type?this.allRight=!0:this.allRight=!1,"flag"==e.className?this.mineNumDom.innerHTML=--this.surplusMine:this.mineNumDom.innerHTML=++this.surplusMine,0==this.surplusMine)if(1==this.allRight)for(alert("恭喜你，游戏通过"),i=0;i<this.tr;i++)for(j=0;j<this.td;j++)this.tds[i][j].onmousedown=null;else alert("游戏失败"),this.gameOver()}},Mine.prototype.gameOver=function(t){for(i=0;i<this.tr;i++)for(j=0;j<this.td;j++)"mine"==this.squares[i][j].type&&(this.tds[i][j].className="mine"),this.tds[i][j].onmousedown=null;t&&(t.style.backgroundColor="#f00")};var btns=document.getElementsByTagName("button"),mine=null,ln=0,arr=[[9,9,10],[16,16,40],[16,30,99]];for(let t=0;t<btns.length-1;t++)btns[t].onclick=function(){btns[ln].className="",this.className="active",(mine=new Mine(arr[t][0],arr[t][1],arr[t][2])).init(),ln=t};btns[0].onclick(),btns[3].onclick=function(){for(var t=0;t<btns.length-1;t++)"active"==btns[t].className&&btns[t].onclick()};	</script></body></html>'''
        html2 = '''<!doctype html><html lang="en"><head><meta charset="UTF-8"><meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" /><meta name="viewport" content="width=540,user-scalable=no"><title>黑白棋</title><style type="text/css">body{background:#c4824d;font-family:"微软雅黑","黑体",serif;margin:0;padding:0}#desk{width:750px;margin:0px auto}#title{float:left;width:60px;padding:15px}#console{float:left;width:110px;padding:10px 0px 0px 10px}h1{margin:10px 0px;color:black;font-size:60px;line-height:70px;font-weight:bold;text-shadow:0px 0px 6px #A33D1B,0px 7px 3px #754B35}h1 span{color:white}.button{margin:15px 0px;width:100px;height:58px;font-size:30px;line-height:58px;color:#440000;background:#dd8e4f;border:1px solid #ff6600;border-radius:30px;box-shadow:0px 4px 10px #482915;text-align:center;cursor:default}.button:hover{background:#E4A774;border:1px solid #ff3300;box-shadow:0px 6px 10px #482915}.button:active{color:#600;background:#eec7a6;border:1px solid #ff0000;box-shadow:0px 2px 5px #482915;position:relative;top:2px}.cbox{border:3px solid transparent;border-radius:10px;width:100px;height:56px}.side{border:3px solid #cc3333;background:#DBA977}.cbox span{float:right;font-size:30px;line-height:54px;font-weight:bold;color:#500;text-shadow:0px 0px 3px #E8C488;padding-right:7px}#interface{position:relative;float:left;width:540px;height:560px}#chessboard{width:522px;height:522px;margin:15px 7px;border:2px solid #CA521E;background:#51150b;box-shadow:0px 8px 15px #482915;-webkit-transform:perspective(740px) rotateX(0deg);transform:perspective(740px) rotateX(0deg);-webkit-transition:-webkit-transform 1s;transition:transform 1s}#chessboard table{background:#835f2e;border-spacing:2px;border:20px solid #51150b}#chessboard td{width:54px;height:54px;border:1px solid #e4c8a9}#chessboard td:hover{border:1px solid #f00}#chessboard .bg0{background:#c1914f}#chessboard .bg1{background:#cba470}.black,.white{width:10px;height:10px;border-radius:50%;margin:5px;padding:17px;box-shadow:0px 4px 10px #482915}.black{background:black;-webkit-transform:rotateY(0deg);transform:rotateY(0deg)}.white{background:white;-webkit-transform:rotateY(180deg);transform:rotateY(180deg)}.reversal{-webkit-transition:-webkit-transform 400ms ease-in-out,background 0ms 200ms;transition:transform 400ms ease-in-out,background 0ms 200ms}.newest:before,.reversal:before{content:"";display:block;width:10px;height:10px;border-radius:5px}.newest:before{background:#f00}.reversal:before{background:#66c}.prompt{width:14px;height:14px;border-radius:50%;margin:20px;padding:0px;background:#FFCC33}#buttons{margin:0px 40px}#buttons div{float:left;margin:0px 10px}#pass,#airuning{position:absolute;top:12px;left:50%;margin-left:-150px;width:300px;height:auto;border-radius:13px;text-align:center;font-size:18px;line-height:26px;background:rgba(230,160,80,0.6);color:#330000;text-shadow:0px 0px 3px #900;display:none}#airuning{top:520px;margin-left:-100px;width:200px}#winner{position:absolute;margin:0 auto;width:100%;height:50px;top:255px;text-align:center;display:none;color:#f20c00;line-height:50px;font-size:30px;background:rgba(230,160,80,0.6);border-radius:25px}@media screen and (max-width:750px){#desk{width:540px}#title{width:100%;padding:0px;text-align:center}#console{width:96%;padding:10px 2%}h1{display:inline-block}.cbox{float:left}#console .button{float:left;margin:0px 5px;width:90px}}</style></head><body><div id="desk"><div id="title"><h1>黑<span>白</span>棋</h1></div><div id="interface"><div id="chessboard"></div><div id="pass"></div><div id="airuning">计算中……</div><div id="winner"></div></div><div id="console"><div id="side1"class="cbox"><span>0</span><div class="black"></div></div><div id="side2"class="cbox"><span>0</span><div class="white"></div></div><div id="play"class="button">开始</div><div id="back"class="button">悔棋</div></div></div><script type="text/javascript">"use strict";function Chessboard(){var e,n,t,a=this;a.toDown=null,a.create=function(){for(var s=document.getElementById("chessboard"),o="<table>",c=0;c<8;c++){o+="<tr>";for(var l=0;l<8;l++)o+="<td class='bg"+(l+c)%2+"'><div></div></td>";o+="</tr>"}o+="</table>",s.innerHTML=o,e=s.getElementsByTagName("div"),function(n){for(var t=0;t<64;t++)!function(t){n[t].onclick=function(){"prompt"==e[t].className&&a.toDown(t)}}(t);n=void 0}(s.getElementsByTagName("td")),n=document.getElementById("console").getElementsByTagName("span"),t={1:document.getElementById("side1"),"-1":document.getElementById("side2")}},a.update=function(a,s){for(var o=0;o<64;o++)e[o].className=["white","","black"][a[o]+1];if(!s)for(var c in a.next)e[c].className="prompt";for(o=0;o<a.newRev.length;o++)e[a.newRev[o]].className+=" reversal";-1!=a.newPos&&(e[a.newPos].className+=" newest"),n[0].innerHTML=a.black,n[1].innerHTML=a.white,t[a.side].className="cbox side",t[-a.side].className="cbox"}}function AI(){var e=this;e.calculateTime=1e3,e.outcomeDepth=14;var r,t,i=15,a=[6,11,2,2,3],n=[{s:0,a:1,b:8,c:9,dr:[1,8]},{s:7,a:6,b:15,c:14,dr:[-1,8]},{s:56,a:57,b:48,c:49,dr:[1,-8]},{s:63,a:62,b:55,c:54,dr:[-1,-8]}];e.history=[[],[]];for(var s=0;s<2;s++)for(var o=0;o<=60;o++)e.history[s][o]=[0,63,7,56,37,26,20,43,19,29,34,44,21,42,45,18,2,61,23,40,5,58,47,16,10,53,22,41,13,46,17,50,51,52,12,11,30,38,25,33,4,3,59,60,39,31,24,32,1,62,15,48,8,55,6,57,9,54,14,49];var c=new Transposition;function f(e){return e>0?1:e<0?-1:0}function u(e){var t=e.black-e.white;return r>=i?1e4*f(t)*e.side:1e4*(t+e.space*f(t))*e.side}function d(e,r,t){var i=-1/0,a=1/0;do{var n=t==i?t+1:t;(t=v(e,r,n-1,n))<n?a=t:i=t}while(i<a);return t<n&&(t=v(e,r,t-1,t)),t}function v(r,i,s,o){if((new Date).getTime()>t)throw new Error("time out");var f=c.get(r.key,i,s,o);if(!1!==f)return f;if(0==r.space)return u(r);if(othe.findLocation(r),0==r.nextNum)return 0==r.prevNum?u(r):(othe.pass(r),-v(r,i,-o,-s));if(i<=0){var d=function(e){for(var r,t=0,i=0,s={},o=0,c=n.length;r=n[o],o<c;o++)if(0!=e[r.s]){t+=15*e[r.s],i+=e[r.s];for(var f=0;f<2;f++)if(!s[r.s+r.dr[f]]){for(var u=!0,d=0,v=1;v<=6;v++){var l=e[r.s+r.dr[f]*v];if(0==l)break;u&&l==e[r.s]?i+=l:(u=!1,d+=l)}7==v&&0!=e[r.s+7*r.dr[f]]&&(i+=d,s[r.s+6*r.dr[f]]=!0)}}else t+=-3*e[r.a],t+=-3*e[r.b],t+=-6*e[r.c];var h=0;for(o=9;o<=54;o+=6==(7&o)?3:1)if(0!=e[o])for(v=0;v<8;v++)if(0==e[othe.dire(o,v)]){h-=e[o];break}var p=(e.nextNum-e.prevNum)*e.side,m=e.space<18?e.space%2==0?-e.side:e.side:0;return(t*a[0]+i*a[1]+h*a[2]+p*a[3]+m*a[4])*e.side}(r);return c.set(r.key,d,i,0,null),d}var p=c.getBest(r.key);null!==p&&l(r.nextIndex,p);for(var m=e.history[1==r.side?0:1][r.space],g=1,k=-1/0,w=null,y=0;y<r.nextNum;y++){var b=r.nextIndex[y],x=-v(othe.newMap(r,b),i-1,-o,-s);if(x>k&&(k=x,w=b,x>s&&(s=x,g=0,h(m,b)),x>=o)){g=2;break}}return l(m,w),c.set(r.key,k,i,g,w),k}function l(e,r){if(e[0]!=r){var t=e.indexOf(r);e.splice(t,1),e.unshift(r)}}function h(e,r){if(e[0]!=r){var t=e.indexOf(r);e[t]=e[t-1],e[t-1]=r}}e.startSearch=function(a){var n=0;if(a.space<=e.outcomeDepth)return t=(new Date).getTime()+6e5,n=(r=a.space)>=i?v(a,r,-1/0,1/0):d(a,r,n),console.log("终局搜索结果：",r,a.space,a.side,n*a.side),c.getBest(a.key);t=(new Date).getTime()+e.calculateTime,r=0;try{for(;r<a.space;){n=d(a,++r,n);var s=c.getBest(a.key);console.log(r,n*a.side,s)}}catch(e){if("time out"!=e.message)throw e}return console.log("搜索结果：",r-1,a.space,a.side,n*a.side),s}}function Transposition(){var e=new Array(524288);this.set=function(t,r,n,a,s){var i=524287&t[0],u=e[i];if(u){if(u.key==t[1]&&u.depth>n)return}else u=e[i]={};u.key=t[1],u.eva=r,u.depth=n,u.flags=a,u.best=s},this.get=function(t,r,n,a){var s=e[524287&t[0]];if(!s||s.key!=t[1]||s.depth<r)return!1;switch(s.flags){case 0:return s.eva;case 1:return s.eva<=n&&s.eva;case 2:return s.eva>=a&&s.eva}},this.getBest=function(t){var r=e[524287&t[0]];return r&&r.key==t[1]?r.best:null}}function Zobrist(){for(var n=[o(),o()],t=[[],[],[]],i=0;i<64;i++)t[0][i]=[o(),o()],t[1][i]=[o(),o()],t[2][i]=[t[0][i][0]^t[1][i][0],t[0][i][1]^t[1][i][1]];function o(){return 4294967296*Math.random()>>0}this.swap=function(t){t[0]^=n[0],t[1]^=n[1]},this.set=function(n,i,o){n[0]^=t[i][o][0],n[1]^=t[i][o][1]}}function Othello(){var e=this,n=[],t=[],i=new Zobrist;e.aiSide=0;var o,r,a,s=!1,c=document.getElementById("airuning"),u=document.getElementById("pass");function d(){var t=e.aiSide==n.side||2==e.aiSide;e.findLocation(n),x(!1),p(!1),board.update(n,t),0==n.space||0==n.nextNum&&0==n.prevNum?o=setTimeout(f,450):0!=n.nextNum?t&&(s=!0,o=setTimeout(function(){x(!0),o=setTimeout(l,50)},400)):o=setTimeout(function(){e.pass(n),d(),p(!0)},450)}function l(){1==n.nextNum?e.go(n.nextIndex[0]):n.space<=58?e.go(ai.startSearch(n)):e.go(n.nextIndex[Math.random()*n.nextIndex.length>>0])}function f(){x(!1),p(!1);var e=document.getElementById("winner");e.style.display="block",e.innerHTML="游戏结束，"+(n.black==n.white?"平局!!!":n.black>n.white?"黑棋胜利!!!":"白棋胜利!!!")}function x(e){c.style.display=e?"block":"none"}function p(e){u.style.display=e?"block":"none",e&&(u.innerHTML=1==n.side?"白方无棋可下，黑方继续下子":"黑方无棋可下，白方继续下子")}e.play=function(){if(!s){clearTimeout(o),console.clear(),n=[];for(var e=0;e<64;e++)n[e]=0;n[28]=n[35]=1,n[27]=n[36]=-1,n.black=n.white=2,n.space=60,n.frontier=[];var i=[18,19,20,21,26,29,34,37,42,43,44,45];for(e=0;e<12;e++)n.frontier[i[e]]=!0;n.side=1,n.newPos=-1,n.newRev=[],n.nextIndex=[],n.next={},n.nextNum=0,n.prevNum=0,n.key=[0,0],t=[],d()}},e.dire=(r=[-8,-7,1,9,8,7,-1,-9],a=[8,0,0,0,8,7,7,7],function(e,n){return 0!=(64&(e+=r[n]))||(7&e)==a[n]?64:e}),e.findLocation=function(n){function t(t,i){for(var o=0;64!=(t=e.dire(t,i))&&n[t]==-n.side;)a[s++]=t,o++;64!=t&&n[t]==n.side||(s-=o)}n.nextIndex=[],n.next=[];for(var i=ai.history[1==n.side?0:1][n.space],o=0;o<60;o++){var r=i[o];if(n.frontier[r]){for(var a=[],s=0,c=0;c<8;c++)t(r,c);s>0&&(s!=a.length&&(a=a.slice(0,s)),n.next[r]=a,n.nextIndex.push(r))}}n.nextNum=n.nextIndex.length},e.pass=function(e){e.side=-e.side,e.prevNum=e.nextNum,i.swap(e.key)},e.newMap=function(n,t){var o=n.slice(0);o[t]=n.side,o.key=n.key.slice(0),i.set(o.key,1==n.side?0:1,t),o.frontier=n.frontier.slice(0),o.frontier[t]=!1;for(var r=0;r<8;r++){var a=e.dire(t,r);64!=a&&0==o[a]&&(o.frontier[a]=!0)}var s=n.next[t],c=s.length;for(r=0;r<c;r++)o[s[r]]=n.side,i.set(o.key,2,s[r]);return 1==n.side?(o.black=n.black+c+1,o.white=n.white-c):(o.white=n.white+c+1,o.black=n.black-c),o.space=64-o.black-o.white,o.side=-n.side,o.prevNum=n.nextNum,i.swap(o.key),o},e.goChess=function(i){t.push(n),e.go(i)},e.go=function(t){s=!1;var i=n.next[t];(n=e.newMap(n,t)).newRev=i,n.newPos=t,d()},e.historyBack=function(){s||0==t.length||(clearTimeout(o),n=t.pop(),d())}}var board=new Chessboard();var ai=new AI();var othe=new Othello();board.create();board.toDown=othe.goChess;document.getElementById("play").onclick=function(){document.getElementById("winner").style.display="none";othe.aiSide=-1;ai.calculateTime=500;ai.outcomeDepth=13;othe.play()};document.getElementById("back").onclick=function(){document.getElementById("winner").style.display="none";othe.historyBack()};</script></body></html>'''
        html3 = '''<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,minimum-scale=1.0,user-scalable=0"><title>2048</title><style> html, body, div, span, applet, object, iframe, h1, h2, h3, h4, h5, h6, p, blockquote, pre, a, abbr, acronym, address, big, cite, code, del, dfn, em, img, ins, kbd, q, s, samp, small, strike, strong, sub, sup, tt, var, b, u, i, center, dl, dt, dd, ol, ul, li, fieldset, form, label, legend, table, caption, tbody, tfoot, thead, tr, th, td, article, aside, canvas, details, embed, figure, figcaption, footer, header, hgroup, menu, nav, output, ruby, section, summary, time, mark, audio, video {margin: 0;padding: 0;border: 0;font-size: 100%;font: inherit;vertical-align: baseline }article, aside, details, figcaption, figure, footer, header, hgroup, menu, nav, section {display: block }body {line-height: 1 }ol, ul {list-style: none }blockquote, q {quotes: none }blockquote:before, blockquote:after, q:before, q:after {content: '';content: none }table {border-collapse: collapse;border-spacing: 0 }@charset "UTF-8";* {box-sizing: border-box;}a {color: #1B9AAA;text-decoration: none;border-bottom: 1px solid currentColor;}a:hover {color: #14727e;}a:focus, a:active {color: #0d4a52;}body, html {position: relative;width: 100%;height: 100%;display: -webkit-box;display: -ms-flexbox;display: flex;-webkit-box-orient: vertical;-webkit-box-direction: normal;-ms-flex-direction: column;flex-direction: column;font-family: "Arvo", Helvetica, sans-serif;font-family: 12px;color: #555;background: #F8FFE5;}strong {font-weight: bold;}p {line-height: 1.6;font-size: 16px;}@media screen and (max-width:400px) {.haiyong{font-size: 12px;}}.inspired {margin-top: 1em;font-size: 0.9rem;color: #9a9a95;}header {color: #F8FFE5;text-align: center;}header span {display: inline-block;box-sizing: border-box;width: 4rem;height: 4rem;line-height: 4rem;margin: 0 0.4rem;background: #FFC43D;}@media screen and (max-width:440px) {header span {width: 3rem;height: 3rem;line-height: 3rem;}}@media screen and (max-width:375px) {header span {width: 2.5rem;height: 2.5rem;line-height: 2.5rem;}}header span:nth-of-type(2) {background: #EF476F;}header span:nth-of-type(3) {background: #1B9AAA;}header span:nth-of-type(4) {background: #06D6A0;}h1 {font-size: 2.2rem;}.directions {padding: 2rem;border-top: 1px solid #9a9a95;border-bottom: 1px solid #9a9a95;}@media screen and (max-width:440px) {.directions{padding: 1rem;}}.container {margin: 0 auto;padding-bottom: 3.5rem;-webkit-box-flex: 1;-ms-flex: 1;flex: 1;width: 100%;max-width: 550px;text-align: center;}header .container {padding: 0;padding: 2rem 4rem;max-width: 900px;}@media screen and (max-width:440px) {header .container {padding: 1rem 2rem;}}.scores {display: -webkit-box;display: -ms-flexbox;display: flex;-webkit-box-pack: center;-ms-flex-pack: center;justify-content: center;}.score-container {display: -webkit-box;display: -ms-flexbox;display: flex;-webkit-box-pack: center;-ms-flex-pack: center;justify-content: center;-webkit-box-align: center;-ms-flex-align: center;align-items: center;margin: 0.8rem;font-size: 1.2rem;line-height: 1;color: #555;}.score-container.best-score {color: #9a9a95;}.score {margin-left: 1rem;position: relative;font-weight: bold;font-size: 1.5rem;vertical-align: middle;text-align: right;}.game {position: relative;margin: 0 auto;background: #9a9a95;padding: 7px;display: inline-block;border-radius: 3px;box-sizing: border-box;}.tile-container {border-radius: 6px;position: relative;width: 270px;height: 270px;}.tile, .background {display: block;color: #F8FFE5;position: absolute;width: 67.5px;height: 67.5px;box-sizing: border-box;text-align: center;}.background {z-index: 1;text-align: center;border: 5px solid #9a9a95;background-color: #F8FFE5;}.tile {opacity: 0;z-index: 2;background: #FFC43D;color: #F8FFE5;display: -webkit-box;display: -ms-flexbox;display: flex;-webkit-box-align: center;-ms-flex-align: center;align-items: center;-webkit-box-pack: center;-ms-flex-pack: center;justify-content: center;font-size: 1.8rem;align-items: center;-webkit-transition: 110ms ease-in-out;transition: 110ms ease-in-out;border-radius: 3px;border: 7px solid #9a9a95;box-sizing: border-box;}.tile--4 {background: #EF476F;color: #F8FFE5;}.tile--8 {background: #1B9AAA;color: #F8FFE5;}.tile--16 {background: #06D6A0;color: #F8FFE5;}.tile--32 {background: #f37694;color: #F8FFE5;}.tile--64 {background: #22c2d6;color: #F8FFE5;}.tile--128 {background: #17f8be;color: #F8FFE5;}.tile--256 {background: #ffd470;color: #F8FFE5;}.tile--512 {background: #eb184a;color: #F8FFE5;}.tile--1024 {background: #14727e;color: #F8FFE5;}.tile--2048 {background: #05a47b;color: #F8FFE5;}.tile--pop {-webkit-animation: pop 0.3s ease-in-out;animation: pop 0.3s ease-in-out;-webkit-animation-fill-mode: forwards;animation-fill-mode: forwards;}.tile--shrink {-webkit-animation: shrink 0.5s ease-in-out;animation: shrink 0.5s ease-in-out;-webkit-animation-fill-mode: forwards;animation-fill-mode: forwards;}.add {position: absolute;opacity: 0;left: 120%;top: 0;font-size: 1rem;color: #1B9AAA;}.add.active {-webkit-animation: add 0.8s ease-in-out;animation: add 0.8s ease-in-out;}@-webkit-keyframes add {0% {opacity: 1;top: 0;}100% {opacity: 0;top: -100%;}}@keyframes add {0% {opacity: 1;top: 0;}100% {opacity: 0;top: -100%;}}@-webkit-keyframes pop {0% {-webkit-transform: scale(0.5);transform: scale(0.5);opacity: 0;}90% {-webkit-transform: scale(1.1);transform: scale(1.1);opacity: 1;}100% {-webkit-transform: scale(1);transform: scale(1);opacity: 1;}}@keyframes pop {0% {-webkit-transform: scale(0.5);transform: scale(0.5);opacity: 0;}90% {-webkit-transform: scale(1.1);transform: scale(1.1);opacity: 1;}100% {-webkit-transform: scale(1);transform: scale(1);opacity: 1;}}@-webkit-keyframes shrink {0% {-webkit-transform: scale(1);transform: scale(1);opacity: 1;}100% {-webkit-transform: scale(0.9);transform: scale(0.9);opacity: 0.9;}}@keyframes shrink {0% {-webkit-transform: scale(1);transform: scale(1);opacity: 1;}100% {-webkit-transform: scale(0.9);transform: scale(0.9);opacity: 0.9;}}.end {opacity: 0;position: absolute;top: 0;left: 0;width: 100%;height: 100%;z-index: -1;display: -webkit-box;display: -ms-flexbox;display: flex;-webkit-box-orient: vertical;-webkit-box-direction: normal;-ms-flex-direction: column;flex-direction: column;-webkit-box-pack: center;-ms-flex-pack: center;justify-content: center;-webkit-box-align: center;-ms-flex-align: center;align-items: center;background: rgba(85, 85, 85, 0.9);color: white;font-size: 2rem;-webkit-transition: opacity 0.3s ease-in-out;transition: opacity 0.3s ease-in-out;}.end btn {margin-top: 1rem;}.end.active {opacity: 1;z-index: 1000;}.monkey {font-size: 3rem;margin: 1rem 0;}.btn {font-family: inherit;font-size: 1rem;border: none;background: #1B9AAA;letter-spacing: 1px;color: white;font-weight: 300;padding: 0.9em 1.5em;border-radius: 3px;border: 1px solid transparent;cursor: pointer;}.btn:hover {background-color: #14727e;}.btn:active {background-color: #0d4a52;}.btn:focus {box-shadow: 0 0 10px #0d4a52 inset;outline: none;}.not-recommended {display: -webkit-box;display: -ms-flexbox;display: flex;-webkit-box-pack: center;-ms-flex-pack: center;justify-content: center;-webkit-box-align: center;-ms-flex-align: center;align-items: center;margin-top: 0.8rem;}.not-recommended *+* {margin-left: 10px;}.not-recommended__item+.not-recommended__annotation:before {font-size: 30px;content: "😐";}.not-recommended__item:hover+.not-recommended__annotation:before {content: "😟";}.not-recommended__item:focus+.not-recommended__annotation:before {content: "😄";}.not-recommended__item:active+.not-recommended__annotation:before {content: "😨";}.page-footer {position: fixed;right: 35px;bottom: 20px;display: flex;align-items: center;padding: 5px;color: black;background: rgba(255, 255, 255, 0.65);}.page-footer a {display: flex;margin-left: 4px;}.touxiang{bottom: 0px;width:30px;height:30px;}</style></head><body><header><div class="container"><h1><span>2</span><span>0</span><span>4</span><span>8</span></h1></div></header><div class="container"><div class="scores"><div class="score-container best-score">历史最佳:<div class="score"><div id="bestScore">0</div></div></div><div class="score-container">分数:<div class="score"><div id="score">0</div><div class="add" id="add"></div></div></div></div><div class="game"><div id="tile-container" class="tile-container"></div><div class="end" id="end">游戏结束<div class="monkey">🙈</div><button class="btn not-recommended__item js-restart-btn" id="try-again">再试一次</button></div></div><div class="not-recommended"><button class="btn not-recommended__item js-restart-btn" id="restart">重新启动游戏</button><span class="not-recommended__annotation"></span></div><br><div class="directions"><p id="haiyong" class="haiyong"><strong>如何玩：</strong> 使用键盘方向键键移动数字方块。相邻的两个方块数字相同，它们可合并成一个！</p></div></div><script>"use strict";var _extends=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var r in n)Object.prototype.hasOwnProperty.call(n,r)&&(e[r]=n[r])}return e},game=null,bestScore=0,scoreDiv=document.getElementById("score"),bestScoreDiv=document.getElementById("bestScore"),addDiv=document.getElementById("add"),endDiv=document.getElementById("end"),size=4,nextId=1,score=0;function initGame(){game=Array(size*size).fill(null),initBestScore()}function initBestScore(){bestScore=localStorage.getItem("bestScore")||0,bestScoreDiv.innerHTML=bestScore}function updateDOM(e,t){var n=getNewElementsDOM(e,t),r=getExistingElementsDOM(e,t);removeElements(getMergedTiles(t)),drawGame(n,!0),drawGame(r)}function removeElements(e){var t=e,n=Array.isArray(t),r=0;for(t=n?t:t[Symbol.iterator]();;){var i;if(n){if(r>=t.length)break;i=t[r++]}else{if((r=t.next()).done)break;i=r.value}var a=i,o=function(){if(c){if(d>=s.length)return"break";u=s[d++]}else{if((d=s.next()).done)return"break";u=d.value}var e=u,t=document.getElementById(e);positionTile(a,t),t.classList.add("tile--shrink"),setTimeout(function(){t.remove()},100)},s=a.mergedIds,c=Array.isArray(s),d=0;for(s=c?s:s[Symbol.iterator]();;){var u;if("break"===o())break}}}function getMergedTiles(e){return e.filter(function(e){return e&&e.mergedIds})}function getNewElementsDOM(e,t){var n=e.filter(function(e){return e}).map(function(e){return e.id});return t.filter(function(e){return e&&-1===n.indexOf(e.id)})}function getExistingElementsDOM(e,t){var n=e.filter(function(e){return e}).map(function(e){return e.id});return t.filter(function(e){return e&&-1!==n.indexOf(e.id)})}function drawBackground(){var e=document.getElementById("tile-container");e.innerHTML="";for(var t=0;t<game.length;t++){game[t];var n=document.createElement("div"),r=t%size,i=Math.floor(t/size);n.style.top=67.5*i+"px",n.style.left=67.5*r+"px",n.classList.add("background"),e.appendChild(n)}}function positionTile(e,t){var n=e.index%size,r=Math.floor(e.index/size);t.style.top=67.5*r+"px",t.style.left=67.5*n+"px"}function drawGame(e,t){for(var n=document.getElementById("tile-container"),r=0;r<e.length;r++){var i=e[r];if(i)if(t)!function(){var e=document.createElement("div");positionTile(i,e),e.classList.add("tile","tile--"+i.value),e.id=i.id,setTimeout(function(){e.classList.add("tile--pop")},i.mergedIds?1:150),e.innerHTML="<p>"+i.value+"</p>",n.appendChild(e)}();else{var a=document.getElementById(i.id);positionTile(i,a)}}}function gameOver(){if(0===game.filter(function(e){return null===e}).length)return!game.find(function(e,t){var n=!(!game[t+1]||(t+1)%4==0)&&e.value===game[t+1].value,r=!!game[t+4]&&e.value===game[t+4].value;return!(!n&&!r)})}function generateNewNumber(){return 100*Math.random()<=90?2:4}function addRandomNumber(){var e=game.map(function(e,t){return t}).filter(function(e){return null===game[e]});if(0!==e.length){var t=e[Math.floor(Math.random()*e.length)],n={id:nextId++,index:t,value:generateNewNumber()};game.splice(t,1,n)}}function getIndexForPoint(e,t){return t*size+e}function reflectGrid(e){for(var t=Array(size*size).fill(0),n=0;n<size;n++)for(var r=0;r<size;r++){var i=getIndexForPoint(r,n),a=getIndexForPoint(size-r-1,n);t[i]=e[a]}return t}function rotateLeft90Deg(e){for(var t=Array(size*size).fill(0),n=0;n<size;n++)for(var r=0;r<size;r++){var i=getIndexForPoint(r,n),a=getIndexForPoint(size-1-n,r);t[i]=e[a]}return t}function rotateRight90Deg(e){for(var t=Array(size*size).fill(0),n=0;n<size;n++)for(var r=0;r<size;r++){var i=getIndexForPoint(r,n),a=getIndexForPoint(n,size-1-r);t[i]=e[a]}return t}function shiftGameRight(e){var t=reflectGrid(e);return reflectGrid(t=shiftGameLeft(t))}function shiftGameLeft(e){for(var t=[],n=0,r=0;r<size;r++){var i=4*r,a=size+4*r,o=e.slice(i,a).filter(function(e){return e}),s=o,c=Array.isArray(s),d=0;for(s=c?s:s[Symbol.iterator]();;){var u;if(c){if(d>=s.length)break;u=s[d++]}else{if((d=s.next()).done)break;u=d.value}delete u.mergedIds}for(var l=0;l<o.length-1;l++)if(o[l].value===o[l+1].value){var m=2*o[l].value;o[l]={id:nextId++,mergedIds:[o[l].id,o[l+1].id],value:m},o.splice(l+1,1),score+=m,n+=m}for(;o.length<size;)o.push(null);t=[].concat(t,o)}return n>0&&(scoreDiv.innerHTML=score,addDiv.innerHTML="+"+n,addDiv.classList.add("active"),setTimeout(function(){addDiv.classList.remove("active")},800),score>bestScore&&(localStorage.setItem("bestScore",score),initBestScore())),t}function shiftGameUp(e){var t=rotateLeft90Deg(e);return rotateRight90Deg(t=shiftGameLeft(t))}function shiftGameDown(e){var t=rotateRight90Deg(e);return rotateLeft90Deg(t=shiftGameLeft(t))}for(var buttons=document.querySelectorAll(".js-restart-btn"),length=buttons.length,i=0;i<length;i++)document.addEventListener?buttons[i].addEventListener("click",function(){newGameStart()}):buttons[i].attachEvent("onclick",function(){newGameStart()});document.addEventListener("keydown",handleKeypress),document.addEventListener("touchstart",handleTouchStart,!1),document.addEventListener("touchmove",handleTouchMove,!1);var xDown=null,yDown=null;function handleTouchStart(e){xDown=e.touches[0].clientX,yDown=e.touches[0].clientY}function handleTouchMove(e){var t=[].concat(game);if(xDown&&yDown){var n=e.touches[0].clientX,r=e.touches[0].clientY,i=xDown-n,a=yDown-r;game=(game=Math.abs(i)>Math.abs(a)?i>0?shiftGameLeft(game):shiftGameRight(game):a>0?shiftGameUp(game):shiftGameDown(game)).map(function(e,t){return e?_extends({},e,{index:t}):null}),addRandomNumber(),updateDOM(t,game),gameOver()?setTimeout(function(){endDiv.classList.add("active")},800):(xDown=null,yDown=null)}}function handleKeypress(e){const t=[37,38,39,40];var n=event.altKey||event.ctrlKey||event.metaKey||event.shiftKey,r=event.which;console.log(r);var i=[].concat(game);if(!n){switch(event.preventDefault(),r){case 37:game=shiftGameLeft(game);break;case 38:game=shiftGameUp(game);break;case 39:game=shiftGameRight(game);break;case 40:game=shiftGameDown(game)}if(game=game.map(function(e,t){return e?_extends({},e,{index:t}):null}),t.includes(r)&&addRandomNumber(),updateDOM(i,game),gameOver())return void setTimeout(function(){endDiv.classList.add("active")},800)}}function newGameStart(){document.getElementById("tile-container").innerHTML="",endDiv.classList.remove("active"),score=0,scoreDiv.innerHTML=score,initGame(),drawBackground();var e=[].concat(game);addRandomNumber(),addRandomNumber(),updateDOM(e,game)}newGameStart();</script></body></html>'''
        return random.choice([html1, html2, html3])
        
    @app.errorhandler(404)
    def page_not_found(e):
        return '''<!DOCTYPE html><html><head><meta charset="utf-8"><title>页面未找到</title><style type="text/css">html,body{margin:0;padding:0;height:100%;min-height:450px;font-family:"Dosis",sans-serif;font-size:32px;font-weight:500;color:#5d7399}.content{height:100%;position:relative;z-index:1;background-color:#d2e1ec;background-image:linear-gradient(to bottom,#bbcfe1 0%,#e8f2f6 80%);overflow:hidden}.snow{position:absolute;top:0;left:0;pointer-events:none;z-index:20}.main-text{padding:20vh 20px 0 20px;text-align:center;line-height:2em;font-size:5vh}.home-link{font-size:0.6em;font-weight:400;color:inherit;text-decoration:none;opacity:0.6;border-bottom:1px dashed rgba(93,115,153,0.5)}.home-link:hover{opacity:1}.ground{height:160px;width:100%;position:absolute;bottom:0;left:0;background:#f6f9fa;box-shadow:0 0 10px 10px#f6f9fa}.ground:before,.ground:after{content:"";display:block;width:250px;height:250px;position:absolute;top:-62.5px;z-index:-1;background:transparent;transform:scaleX(0.2)rotate(45deg)}.ground:after{left:50%;margin-left:-166.6666666667px;box-shadow:-340px 260px 15px#bac4d5,-625px 575px 15px#91a1bc,-855px 945px 15px#7e90b0,-1165px 1235px 15px#b0bccf,-1470px 1530px 15px#94a3be,-1750px 1850px 15px#91a1bc,-2145px 2055px 15px#b0bccf,-2400px 2400px 15px#7e90b0,-2665px 2735px 15px#a7b4c9,-2965px 3035px 15px#8496b4,-3260px 3340px 15px#94a3be,-3580px 3620px 15px#97a6c0,-3885px 3915px 15px#9aa9c2,-4160px 4240px 15px#8193b2,-4470px 4530px 15px#8e9eba,-4845px 4755px 15px#7e90b0}.ground:before{right:50%;margin-right:-166.6666666667px;box-shadow:260px-340px 15px#b0bccf,630px-570px 15px#a1aec6,925px-875px 15px#94a3be,1170px-1230px 15px#a7b4c9,1535px-1465px 15px#a7b4c9,1845px-1755px 15px#8a9bb8,2150px-2050px 15px#b7c1d3,2445px-2355px 15px#8798b6,2735px-2665px 15px#bac4d5,3015px-2985px 15px#94a3be,3270px-3330px 15px#b7c1d3,3620px-3580px 15px#8193b2,3860px-3940px 15px#9dabc4,4215px-4185px 15px#8798b6,4485px-4515px 15px#8e9eba,4810px-4790px 15px#bac4d5}.mound{margin-top:-100px;font-weight:800;font-size:180px;text-align:center;color:#dd4040;pointer-events:none}.mound:before{content:"";display:block;width:600px;height:200px;position:absolute;left:50%;margin-left:-300px;top:50px;z-index:1;border-radius:100%;background-color:#e8f2f6;background-image:linear-gradient(to bottom,#dee8f1,#f6f9fa 60px)}.mound:after{content:"";display:block;width:28px;height:6px;position:absolute;left:50%;margin-left:-150px;top:68px;z-index:2;background:#dd4040;border-radius:100%;transform:rotate(-15deg);box-shadow:-56px 12px 0 1px#dd4040,-126px 6px 0 2px#dd4040,-196px 24px 0 3px#dd4040}.mound_text{transform:rotate(10deg)}.mound_spade{display:block;width:35px;height:30px;position:absolute;right:50%;top:42%;margin-right:-250px;z-index:0;transform:rotate(35deg);background:#dd4040}.mound_spade:before,.mound_spade:after{content:"";display:block;position:absolute}.mound_spade:before{width:40%;height:30px;bottom:98%;left:50%;margin-left:-20%;background:#dd4040}.mound_spade:after{width:100%;height:30px;top:-55px;left:0%;box-sizing:border-box;border:10px solid#dd4040;border-radius:4px 4px 20px 20px}</style></head><body><div class="content"><canvas class="snow"id="snow"></canvas><div class="main-text"><h2>哎呀！<br/>你访问的页面走丢啦！</h1></div><div class="ground"><div class="mound"><div class="mound_text">404</div><div class="mound_spade"></div></div></div></div><script type="text/javascript">(function(){function ready(fn){if (document.readyState!='loading'){fn();}else{document.addEventListener('DOMContentLoaded', fn);}}function makeSnow(el){var ctx=el.getContext('2d');var width=0;var height=0;var particles=[];var Particle=function(){this.x=this.y=this.dx=this.dy=0;this.reset();}
                  Particle.prototype.reset=function(){this.y=Math.random()*height;this.x=Math.random()*width;this.dx=(Math.random()*1)-0.5;this.dy=(Math.random()*0.5)+0.5;}
                  function createParticles(count){if (count!=particles.length) {particles=[];for(var i=0;i<count;i++){particles.push(new Particle());}}}function onResize(){width=window.innerWidth;height=window.innerHeight;el.width=width;el.height=height;createParticles((width*height)/10000);}function updateParticles(){ctx.clearRect(0,0,width,height);ctx.fillStyle='#f6f9fa';particles.forEach(function(particle){particle.y+=particle.dy;particle.x+=particle.dx;if(particle.y>height){particle.y=0;}if(particle.x>width){particle.reset();particle.y=0;}ctx.beginPath();ctx.arc(particle.x,particle.y,5,0,Math.PI*2,false);ctx.fill();});window.requestAnimationFrame(updateParticles);}onResize();updateParticles();window.addEventListener('resize',onResize);}ready(function(){var canvas=document.getElementById('snow');makeSnow(canvas);});})();</script></body></html>
               '''
        
    @app.route('/receivefile')
    def receivefile():
        return '''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>文件上传</title><style> body{padding:0;margin:0;}.file-upload {width: calc(98vw - 12px);padding: 5px;border: 1px solid #999;border-radius: 5px;text-align: center;margin:10px auto;}.button-63 {align-items: center;background-image: linear-gradient(144deg,#AF40FF, #5B42F3 50%,#00DDEB);border: 0;border-radius: 8px;box-shadow: rgba(151, 65, 252, 0.2) 0 15px 30px -5px;box-sizing: border-box;color: #FFFFFF;display: flex;font-family: Phantomsans, sans-serif;font-size: 20px;justify-content: center;line-height: 1em;max-width: 100%;min-width: 140px;padding: 19px 24px;text-decoration: none;user-select: none;-webkit-user-select: none;touch-action: manipulation;white-space: nowrap;cursor: pointer;margin-left: auto;margin-right: auto;}.button-63:active, .button-63:hover {outline: 0;}@media (min-width: 768px) {.button-63 {font-size: 24px;min-width: 196px;}}.button-85 {margin-left:20px;padding: 0.6em 2em;border: none;outline: none;color: rgb(255, 255, 255);background: #111;cursor: pointer;position: relative;z-index: 0;border-radius: 10px;user-select: none;-webkit-user-select: none;touch-action: manipulation;}.button-85:before {content: "";background: linear-gradient( 45deg, #ff0000, #ff7300, #fffb00, #48ff00, #00ffd5, #002bff, #7a00ff, #ff00c8, #ff0000 );position: absolute;top: -2px;left: -2px;background-size: 400%;z-index: -1;filter: blur(5px);-webkit-filter: blur(5px);width: calc(100% + 4px);height: calc(100% + 4px);animation: glowing-button-85 20s linear infinite;transition: opacity 0.3s ease-in-out;border-radius: 10px;}@keyframes glowing-button-85 {0% {background-position: 0 0;}50% {background-position: 400% 0;}100% {background-position: 0 0;}}.button-85:after {z-index: -1;content: "";position: absolute;width: 100%;height: 100%;background: #222;left: 0;top: 0;border-radius: 10px;}.file {position: relative;display: inline-block;background: #D0EEFF;border: 1px solid #99D3F5;border-radius: 4px;padding: 4px 12px;overflow: hidden;color: #1E88C7;text-decoration: none;text-indent: 0;line-height: 20px;}.file input {position: absolute;font-size: 100px;right: 0;top: 0;opacity: 0;}.file:hover {background: #AADFFD;border-color: #78C3F3;color: #004974;text-decoration: none;}.progress-bar-container {width: 100%;height: 20px;border: 1px solid #ccc;border-radius: 5px;overflow: hidden;margin-top: 10px;}.progress-bar {height: 100%;width: 0;background-color: #4CAF50;transition: width 0.3s ease-in-out;}.file-list {text-align: left;margin-top: 10px;}ul {list-style-type: none;margin: 0;padding: 0;}li {background-color: #f2f2f2;border: 1px solid #ddd;margin: 10px 0;padding: 10px;text-align: center;}</style></head><body><div class="file-upload"><div id="progressContainer" class="progress-bar-container" style="display: none;"><div id="progressBar" class="progress-bar"></div></div><h1>文件上传</h1><a href="javascript:;" class="file">选择文件<input type="file" id="fileInput" multiple></a><h6>或拖拽文件至此</h6><div class="file-list" id="fileList" style="display: none;"><ul id="fileListItems"></ul></div><button class="button-63" role="button" id="uploadButton" style="display: none;">开始上传</button></div><script>document.getElementById("fileInput").addEventListener("change",function(){var e=document.getElementById("fileList"),t=document.getElementById("fileListItems");if(t.innerHTML="",0===this.files.length)return e.style.display="none",void(document.getElementById("uploadButton").style.display="none");for(var n=0;n<this.files.length;n++){var l=document.createElement("li"),a=document.createElement("span");a.innerText=this.files[n].name;var d=document.createElement("button");d.innerText="删除",d.classList.add("button-85"),d.setAttribute("data-index",n),d.addEventListener("click",function(){var e=parseInt(this.getAttribute("data-index")),t=Array.from(document.getElementById("fileInput").files);t.splice(e,1);for(var n=new ClipboardEvent("").clipboardData||new DataTransfer,l=0;l<t.length;l++)n.items.add(t[l]);document.getElementById("fileInput").files=n.files,document.getElementById("fileInput").dispatchEvent(new Event("change"))}),l.appendChild(a),l.appendChild(d),t.appendChild(l)}e.style.display="block",document.getElementById("uploadButton").style.display="block"});var fileUploadArea=document.querySelector(".file-upload");fileUploadArea.addEventListener("dragover",function(e){e.preventDefault(),this.classList.add("dragover")}),fileUploadArea.addEventListener("dragleave",function(){this.classList.remove("dragover")}),fileUploadArea.addEventListener("drop",function(e){e.preventDefault(),this.classList.remove("dragover");var t=e.dataTransfer.files,n=document.getElementById("fileListItems");if(n.innerHTML="",0===t.length)return document.getElementById("fileList").style.display="none",void(document.getElementById("uploadButton").style.display="none");for(var l=0;l<t.length;l++){var a=document.createElement("li"),d=document.createElement("span");d.innerText=t[l].name;var i=document.createElement("button");i.innerText="删除",i.classList.add("button-85"),i.setAttribute("data-index",l),i.addEventListener("click",function(){var e=parseInt(this.getAttribute("data-index")),t=Array.from(document.getElementById("fileInput").files);t.splice(e,1);for(var n=new ClipboardEvent("").clipboardData||new DataTransfer,l=0;l<t.length;l++)n.items.add(t[l]);document.getElementById("fileInput").files=n.files,document.getElementById("fileInput").dispatchEvent(new Event("change"))}),a.appendChild(d),a.appendChild(i),n.appendChild(a)}document.getElementById("fileList").style.display="block",document.getElementById("uploadButton").style.display="block",document.getElementById("fileInput").files=t}),document.getElementById("uploadButton").addEventListener("click",function(){this.style.display="none";for(var e=document.getElementsByClassName("button-85"),t=0;t<e.length;t++){e[t].style.display="none"}var n=document.getElementById("fileInput").files;if(0!==n.length){var l=new XMLHttpRequest,a=document.getElementById("progressContainer"),d=document.getElementById("progressBar");l.upload.addEventListener("progress",function(e){var t=e.loaded/e.total*100;d.style.width=t.toFixed(2)+"%"}),l.onreadystatechange=function(){if(l.readyState===XMLHttpRequest.DONE){if(200===l.status){var e=JSON.parse(l.responseText);console.log(e),d.style.width="0%";for(var t="",n=0;n<e.length;n++){if("success"===e[n].status)var i=e[n].filename+'<span style="color:#0f0;">上传成功</span>';else i=e[n].filename+'<span style="color:#f00;">上传失败</span>';t=t+"<li>"+i+"</li>"}}else alert("上传失败");a.style.display="none",fileListItems.innerHTML=t}},a.style.display="block",l.open("POST","/upload",!0);for(var i=new FormData,s=0;s<n.length;s++)i.append("file",n[s]);l.send(i)}else alert("未选择文件")});</script></body></html>'''

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
            return "文件不存在", 404
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
        (r"Directory\shell\Receive File", "接收文件至此目录", epath + ' R "%1"'),
        (r"Directory\Background\shell\Receive File", "接收文件至此目录", epath + ' R "%v"')
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
        r"Folder\shell\Receive File",
        r"Directory\Background\shell\Receive File"
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
    elif args[1] == "R":
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
        
