
/* Merged Plone Javascript file
 * This file is dynamically assembled from separate parts.
 * Some of these parts have 3rd party licenses or copyright information attached
 * Such information is valid for that section,
 * not for the entire composite file
 * originating files are separated by - filename.js -
 */

/* - ++resource++collective.flowplayer/flowplayer.min.js - */
/*
 * flowplayer.js 3.2.11. The Flowplayer API
 *
 * Copyright 2009-2011 Flowplayer Oy
 *
 * This file is part of Flowplayer.
 *
 * Flowplayer is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * Flowplayer is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with Flowplayer.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Date: 2012-06-16 10:34:45 -0400 (Sat, 16 Jun 2012)
 * Revision: 808
 */
(function(){function g(o){console.log("$f.fireEvent",[].slice.call(o))}function k(q){if(!q||typeof q!="object"){return q}var o=new q.constructor();for(var p in q){if(q.hasOwnProperty(p)){o[p]=k(q[p])}}return o}function m(t,q){if(!t){return}var o,p=0,r=t.length;if(r===undefined){for(o in t){if(q.call(t[o],o,t[o])===false){break}}}else{for(var s=t[0];p<r&&q.call(s,p,s)!==false;s=t[++p]){}}return t}function c(o){return document.getElementById(o)}function i(q,p,o){if(typeof p!="object"){return q}if(q&&p){m(p,function(r,s){if(!o||typeof s!="function"){q[r]=s}})}return q}function n(s){var q=s.indexOf(".");if(q!=-1){var p=s.slice(0,q)||"*";var o=s.slice(q+1,s.length);var r=[];m(document.getElementsByTagName(p),function(){if(this.className&&this.className.indexOf(o)!=-1){r.push(this)}});return r}}function f(o){o=o||window.event;if(o.preventDefault){o.stopPropagation();o.preventDefault()}else{o.returnValue=false;o.cancelBubble=true}return false}function j(q,o,p){q[o]=q[o]||[];q[o].push(p)}function e(){return"_"+(""+Math.random()).slice(2,10)}var h=function(t,r,s){var q=this,p={},u={};q.index=r;if(typeof t=="string"){t={url:t}}i(this,t,true);m(("Begin*,Start,Pause*,Resume*,Seek*,Stop*,Finish*,LastSecond,Update,BufferFull,BufferEmpty,BufferStop").split(","),function(){var v="on"+this;if(v.indexOf("*")!=-1){v=v.slice(0,v.length-1);var w="onBefore"+v.slice(2);q[w]=function(x){j(u,w,x);return q}}q[v]=function(x){j(u,v,x);return q};if(r==-1){if(q[w]){s[w]=q[w]}if(q[v]){s[v]=q[v]}}});i(this,{onCuepoint:function(x,w){if(arguments.length==1){p.embedded=[null,x];return q}if(typeof x=="number"){x=[x]}var v=e();p[v]=[x,w];if(s.isLoaded()){s._api().fp_addCuepoints(x,r,v)}return q},update:function(w){i(q,w);if(s.isLoaded()){s._api().fp_updateClip(w,r)}var v=s.getConfig();var x=(r==-1)?v.clip:v.playlist[r];i(x,w,true)},_fireEvent:function(v,y,w,A){if(v=="onLoad"){m(p,function(B,C){if(C[0]){s._api().fp_addCuepoints(C[0],r,B)}});return false}A=A||q;if(v=="onCuepoint"){var z=p[y];if(z){return z[1].call(s,A,w)}}if(y&&"onBeforeBegin,onMetaData,onStart,onUpdate,onResume".indexOf(v)!=-1){i(A,y);if(y.metaData){if(!A.duration){A.duration=y.metaData.duration}else{A.fullDuration=y.metaData.duration}}}var x=true;m(u[v],function(){x=this.call(s,A,y,w)});return x}});if(t.onCuepoint){var o=t.onCuepoint;q.onCuepoint.apply(q,typeof o=="function"?[o]:o);delete t.onCuepoint}m(t,function(v,w){if(typeof w=="function"){j(u,v,w);delete t[v]}});if(r==-1){s.onCuepoint=this.onCuepoint}};var l=function(p,r,q,t){var o=this,s={},u=false;if(t){i(s,t)}m(r,function(v,w){if(typeof w=="function"){s[v]=w;delete r[v]}});i(this,{animate:function(y,z,x){if(!y){return o}if(typeof z=="function"){x=z;z=500}if(typeof y=="string"){var w=y;y={};y[w]=z;z=500}if(x){var v=e();s[v]=x}if(z===undefined){z=500}r=q._api().fp_animate(p,y,z,v);return o},css:function(w,x){if(x!==undefined){var v={};v[w]=x;w=v}r=q._api().fp_css(p,w);i(o,r);return o},show:function(){this.display="block";q._api().fp_showPlugin(p);return o},hide:function(){this.display="none";q._api().fp_hidePlugin(p);return o},toggle:function(){this.display=q._api().fp_togglePlugin(p);return o},fadeTo:function(y,x,w){if(typeof x=="function"){w=x;x=500}if(w){var v=e();s[v]=w}this.display=q._api().fp_fadeTo(p,y,x,v);this.opacity=y;return o},fadeIn:function(w,v){return o.fadeTo(1,w,v)},fadeOut:function(w,v){return o.fadeTo(0,w,v)},getName:function(){return p},getPlayer:function(){return q},_fireEvent:function(w,v,x){if(w=="onUpdate"){var z=q._api().fp_getPlugin(p);if(!z){return}i(o,z);delete o.methods;if(!u){m(z.methods,function(){var B=""+this;o[B]=function(){var C=[].slice.call(arguments);var D=q._api().fp_invoke(p,B,C);return D==="undefined"||D===undefined?o:D}});u=true}}var A=s[w];if(A){var y=A.apply(o,v);if(w.slice(0,1)=="_"){delete s[w]}return y}return o}})};function b(q,G,t){var w=this,v=null,D=false,u,s,F=[],y={},x={},E,r,p,C,o,A;i(w,{id:function(){return E},isLoaded:function(){return(v!==null&&v.fp_play!==undefined&&!D)},getParent:function(){return q},hide:function(H){if(H){q.style.height="0px"}if(w.isLoaded()){v.style.height="0px"}return w},show:function(){q.style.height=A+"px";if(w.isLoaded()){v.style.height=o+"px"}return w},isHidden:function(){return w.isLoaded()&&parseInt(v.style.height,10)===0},load:function(J){if(!w.isLoaded()&&w._fireEvent("onBeforeLoad")!==false){var H=function(){if(u&&!flashembed.isSupported(G.version)){q.innerHTML=""}if(J){J.cached=true;j(x,"onLoad",J)}flashembed(q,G,{config:t})};var I=0;m(a,function(){this.unload(function(K){if(++I==a.length){H()}})})}return w},unload:function(J){if(u.replace(/\s/g,"")!==""){if(w._fireEvent("onBeforeUnload")===false){if(J){J(false)}return w}D=true;try{if(v){if(v.fp_isFullscreen()){v.fp_toggleFullscreen()}v.fp_close();w._fireEvent("onUnload")}}catch(H){}var I=function(){v=null;q.innerHTML=u;D=false;if(J){J(true)}};if(/WebKit/i.test(navigator.userAgent)&&!/Chrome/i.test(navigator.userAgent)){setTimeout(I,0)}else{I()}}else{if(J){J(false)}}return w},getClip:function(H){if(H===undefined){H=C}return F[H]},getCommonClip:function(){return s},getPlaylist:function(){return F},getPlugin:function(H){var J=y[H];if(!J&&w.isLoaded()){var I=w._api().fp_getPlugin(H);if(I){J=new l(H,I,w);y[H]=J}}return J},getScreen:function(){return w.getPlugin("screen")},getControls:function(){return w.getPlugin("controls")._fireEvent("onUpdate")},getLogo:function(){try{return w.getPlugin("logo")._fireEvent("onUpdate")}catch(H){}},getPlay:function(){return w.getPlugin("play")._fireEvent("onUpdate")},getConfig:function(H){return H?k(t):t},getFlashParams:function(){return G},loadPlugin:function(K,J,M,L){if(typeof M=="function"){L=M;M={}}var I=L?e():"_";w._api().fp_loadPlugin(K,J,M,I);var H={};H[I]=L;var N=new l(K,null,w,H);y[K]=N;return N},getState:function(){return w.isLoaded()?v.fp_getState():-1},play:function(I,H){var J=function(){if(I!==undefined){w._api().fp_play(I,H)}else{w._api().fp_play()}};if(w.isLoaded()){J()}else{if(D){setTimeout(function(){w.play(I,H)},50)}else{w.load(function(){J()})}}return w},getVersion:function(){var I="flowplayer.js 3.2.11";if(w.isLoaded()){var H=v.fp_getVersion();H.push(I);return H}return I},_api:function(){if(!w.isLoaded()){throw"Flowplayer "+w.id()+" not loaded when calling an API method"}return v},setClip:function(H){m(H,function(I,J){if(typeof J=="function"){j(x,I,J);delete H[I]}else{if(I=="onCuepoint"){$f(q).getCommonClip().onCuepoint(H[I][0],H[I][1])}}});w.setPlaylist([H]);return w},getIndex:function(){return p},bufferAnimate:function(H){v.fp_bufferAnimate(H===undefined||H);return w},_swfHeight:function(){return v.clientHeight}});m(("Click*,Load*,Unload*,Keypress*,Volume*,Mute*,Unmute*,PlaylistReplace,ClipAdd,Fullscreen*,FullscreenExit,Error,MouseOver,MouseOut").split(","),function(){var H="on"+this;if(H.indexOf("*")!=-1){H=H.slice(0,H.length-1);var I="onBefore"+H.slice(2);w[I]=function(J){j(x,I,J);return w}}w[H]=function(J){j(x,H,J);return w}});m(("pause,resume,mute,unmute,stop,toggle,seek,getStatus,getVolume,setVolume,getTime,isPaused,isPlaying,startBuffering,stopBuffering,isFullscreen,toggleFullscreen,reset,close,setPlaylist,addClip,playFeed,setKeyboardShortcutsEnabled,isKeyboardShortcutsEnabled").split(","),function(){var H=this;w[H]=function(J,I){if(!w.isLoaded()){return w}var K=null;if(J!==undefined&&I!==undefined){K=v["fp_"+H](J,I)}else{K=(J===undefined)?v["fp_"+H]():v["fp_"+H](J)}return K==="undefined"||K===undefined?w:K}});w._fireEvent=function(Q){if(typeof Q=="string"){Q=[Q]}var R=Q[0],O=Q[1],M=Q[2],L=Q[3],K=0;if(t.debug){g(Q)}if(!w.isLoaded()&&R=="onLoad"&&O=="player"){v=v||c(r);o=w._swfHeight();m(F,function(){this._fireEvent("onLoad")});m(y,function(S,T){T._fireEvent("onUpdate")});s._fireEvent("onLoad")}if(R=="onLoad"&&O!="player"){return}if(R=="onError"){if(typeof O=="string"||(typeof O=="number"&&typeof M=="number")){O=M;M=L}}if(R=="onContextMenu"){m(t.contextMenu[O],function(S,T){T.call(w)});return}if(R=="onPluginEvent"||R=="onBeforePluginEvent"){var H=O.name||O;var I=y[H];if(I){I._fireEvent("onUpdate",O);return I._fireEvent(M,Q.slice(3))}return}if(R=="onPlaylistReplace"){F=[];var N=0;m(O,function(){F.push(new h(this,N++,w))})}if(R=="onClipAdd"){if(O.isInStream){return}O=new h(O,M,w);F.splice(M,0,O);for(K=M+1;K<F.length;K++){F[K].index++}}var P=true;if(typeof O=="number"&&O<F.length){C=O;var J=F[O];if(J){P=J._fireEvent(R,M,L)}if(!J||P!==false){P=s._fireEvent(R,M,L,J)}}m(x[R],function(){P=this.call(w,O,M);if(this.cached){x[R].splice(K,1)}if(P===false){return false}K++});return P};function B(){if($f(q)){$f(q).getParent().innerHTML="";p=$f(q).getIndex();a[p]=w}else{a.push(w);p=a.length-1}A=parseInt(q.style.height,10)||q.clientHeight;E=q.id||"fp"+e();r=G.id||E+"_api";G.id=r;u=q.innerHTML;if(typeof t=="string"){t={clip:{url:t}}}t.playerId=E;t.clip=t.clip||{};if(q.getAttribute("href",2)&&!t.clip.url){t.clip.url=q.getAttribute("href",2)}s=new h(t.clip,-1,w);t.playlist=t.playlist||[t.clip];var I=0;m(t.playlist,function(){var L=this;if(typeof L=="object"&&L.length){L={url:""+L}}m(t.clip,function(M,N){if(N!==undefined&&L[M]===undefined&&typeof N!="function"){L[M]=N}});t.playlist[I]=L;L=new h(L,I,w);F.push(L);I++});m(t,function(L,M){if(typeof M=="function"){if(s[L]){s[L](M)}else{j(x,L,M)}delete t[L]}});m(t.plugins,function(L,M){if(M){y[L]=new l(L,M,w)}});if(!t.plugins||t.plugins.controls===undefined){y.controls=new l("controls",null,w)}y.canvas=new l("canvas",null,w);u=q.innerHTML;function K(L){if(/iPad|iPhone|iPod/i.test(navigator.userAgent)&&!/.flv$/i.test(F[0].url)&&!J()){return true}if(!w.isLoaded()&&w._fireEvent("onBeforeClick")!==false){w.load()}return f(L)}function J(){return w.hasiPadSupport&&w.hasiPadSupport()}function H(){if(u.replace(/\s/g,"")!==""){if(q.addEventListener){q.addEventListener("click",K,false)}else{if(q.attachEvent){q.attachEvent("onclick",K)}}}else{if(q.addEventListener&&!J()){q.addEventListener("click",f,false)}w.load()}}setTimeout(H,0)}if(typeof q=="string"){var z=c(q);if(!z){throw"Flowplayer cannot access element: "+q}q=z;B()}else{B()}}var a=[];function d(o){this.length=o.length;this.each=function(q){m(o,q)};this.size=function(){return o.length};var p=this;for(name in b.prototype){p[name]=function(){var q=arguments;p.each(function(){this[name].apply(this,q)})}}}window.flowplayer=window.$f=function(){var p=null;var o=arguments[0];if(!arguments.length){m(a,function(){if(this.isLoaded()){p=this;return false}});return p||a[0]}if(arguments.length==1){if(typeof o=="number"){return a[o]}else{if(o=="*"){return new d(a)}m(a,function(){if(this.id()==o.id||this.id()==o||this.getParent()==o){p=this;return false}});return p}}if(arguments.length>1){var t=arguments[1],q=(arguments.length==3)?arguments[2]:{};if(typeof t=="string"){t={src:t}}t=i({bgcolor:"#000000",version:[10,1],expressInstall:"http://releases.flowplayer.org/swf/expressinstall.swf",cachebusting:false},t);if(typeof o=="string"){if(o.indexOf(".")!=-1){var s=[];m(n(o),function(){s.push(new b(this,k(t),k(q)))});return new d(s)}else{var r=c(o);return new b(r!==null?r:k(o),k(t),k(q))}}else{if(o){return new b(o,k(t),k(q))}}}return null};i(window.$f,{fireEvent:function(){var o=[].slice.call(arguments);var q=$f(o[0]);return q?q._fireEvent(o.slice(1)):null},addPlugin:function(o,p){b.prototype[o]=p;return $f},each:m,extend:i});if(typeof jQuery=="function"){jQuery.fn.flowplayer=function(q,p){if(!arguments.length||typeof arguments[0]=="number"){var o=[];this.each(function(){var r=$f(this);if(r){o.push(r)}});return arguments.length?o[arguments[0]]:new d(o)}return this.each(function(){$f(this,k(q),p?k(p):{})})}}})();(function(){var h=document.all,j="http://get.adobe.com/flashplayer",c=typeof jQuery=="function",e=/(\d+)[^\d]+(\d+)[^\d]*(\d*)/,b={width:"100%",height:"100%",id:"_"+(""+Math.random()).slice(9),allowfullscreen:true,allowscriptaccess:"always",quality:"high",version:[3,0],onFail:null,expressInstall:null,w3c:false,cachebusting:false};if(window.attachEvent){window.attachEvent("onbeforeunload",function(){__flash_unloadHandler=function(){};__flash_savedUnloadHandler=function(){}})}function i(m,l){if(l){for(var f in l){if(l.hasOwnProperty(f)){m[f]=l[f]}}}return m}function a(f,n){var m=[];for(var l in f){if(f.hasOwnProperty(l)){m[l]=n(f[l])}}return m}window.flashembed=function(f,m,l){if(typeof f=="string"){f=document.getElementById(f.replace("#",""))}if(!f){return}if(typeof m=="string"){m={src:m}}return new d(f,i(i({},b),m),l)};var g=i(window.flashembed,{conf:b,getVersion:function(){var m,f;try{f=navigator.plugins["Shockwave Flash"].description.slice(16)}catch(o){try{m=new ActiveXObject("ShockwaveFlash.ShockwaveFlash.7");f=m&&m.GetVariable("$version")}catch(n){try{m=new ActiveXObject("ShockwaveFlash.ShockwaveFlash.6");f=m&&m.GetVariable("$version")}catch(l){}}}f=e.exec(f);return f?[1*f[1],1*f[(f[1]*1>9?2:3)]*1]:[0,0]},asString:function(l){if(l===null||l===undefined){return null}var f=typeof l;if(f=="object"&&l.push){f="array"}switch(f){case"string":l=l.replace(new RegExp('(["\\\\])',"g"),"\\$1");l=l.replace(/^\s?(\d+\.?\d*)%/,"$1pct");return'"'+l+'"';case"array":return"["+a(l,function(o){return g.asString(o)}).join(",")+"]";case"function":return'"function()"';case"object":var m=[];for(var n in l){if(l.hasOwnProperty(n)){m.push('"'+n+'":'+g.asString(l[n]))}}return"{"+m.join(",")+"}"}return String(l).replace(/\s/g," ").replace(/\'/g,'"')},getHTML:function(o,l){o=i({},o);var n='<object width="'+o.width+'" height="'+o.height+'" id="'+o.id+'" name="'+o.id+'"';if(o.cachebusting){o.src+=((o.src.indexOf("?")!=-1?"&":"?")+Math.random())}if(o.w3c||!h){n+=' data="'+o.src+'" type="application/x-shockwave-flash"'}else{n+=' classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000"'}n+=">";if(o.w3c||h){n+='<param name="movie" value="'+o.src+'" />'}o.width=o.height=o.id=o.w3c=o.src=null;o.onFail=o.version=o.expressInstall=null;for(var m in o){if(o[m]){n+='<param name="'+m+'" value="'+o[m]+'" />'}}var p="";if(l){for(var f in l){if(l[f]){var q=l[f];p+=f+"="+(/function|object/.test(typeof q)?g.asString(q):q)+"&"}}p=p.slice(0,-1);n+='<param name="flashvars" value=\''+p+"' />"}n+="</object>";return n},isSupported:function(f){return k[0]>f[0]||k[0]==f[0]&&k[1]>=f[1]}});var k=g.getVersion();function d(f,n,m){if(g.isSupported(n.version)){f.innerHTML=g.getHTML(n,m)}else{if(n.expressInstall&&g.isSupported([6,65])){f.innerHTML=g.getHTML(i(n,{src:n.expressInstall}),{MMredirectURL:encodeURIComponent(location.href),MMplayerType:"PlugIn",MMdoctitle:document.title})}else{if(!f.innerHTML.replace(/\s/g,"")){f.innerHTML="<h2>Flash version "+n.version+" or greater is required</h2><h3>"+(k[0]>0?"Your version is "+k:"You have no flash plugin installed")+"</h3>"+(f.tagName=="A"?"<p>Click here to download latest version</p>":"<p>Download latest version from <a href='"+j+"'>here</a></p>");if(f.tagName=="A"||f.tagName=="DIV"){f.onclick=function(){location.href=j}}}if(n.onFail){var l=n.onFail.call(this);if(typeof l=="string"){f.innerHTML=l}}}}if(h){window[n.id]=document.getElementById(n.id)}i(this,{getRoot:function(){return f},getOptions:function(){return n},getConf:function(){return m},getApi:function(){return f.firstChild}})}if(c){jQuery.tools=jQuery.tools||{version:"3.2.11"};jQuery.tools.flashembed={conf:b};jQuery.fn.flashembed=function(l,f){return this.each(function(){$(this).data("flashembed",flashembed(this,l,f))})}}})();

/* - ++resource++collective.flowplayer/flowplayer.playlist.min.js - */
/*
 * flowplayer.playlist Flowplayer playlist plugin.
 *
 * This file is part of Flowplayer, http://flowplayer.org
 *
 * Author: Tero Piirainen, <info@flowplayer.org>
 * Copyright (c) 2008-2012 Flowplayer Ltd
 *
 * Released under the MIT License:
 * http://www.opensource.org/licenses/mit-license.php
 *
 */
(function(a){$f.addPlugin("playlist",function(g,d){var j=this;var i={playingClass:"playing",pausedClass:"paused",progressClass:"progress",stoppedClass:"stopped",template:'<a href="${url}">${title}</a>',loop:false,continuousPlay:false,playOnClick:true,manual:false};a.extend(i,d);g=a(g);var f=l();var b=i.manual||(f.length>0&&!g.html().match(/\$/));var s=null;function m(v){var u=s;a.each(v,function(w,x){if(!a.isFunction(x)){u=u.replace("${"+w+"}",x).replace("$%7B"+w+"%7D",x)}});return u}function c(){f=l().unbind("click.playlist").bind("click.playlist",function(){return q(a(this),f.index(this))})}function n(){g.empty();a.each(j.getPlaylist(),function(){g.append(m(this))});c()}function q(u,v){if(u.hasClass(i.playingClass)||u.hasClass(i.pausedClass)){j.toggle()}else{u.addClass(i.progressClass);j.play(v)}return false}function e(){if(b){f=l()}f.removeClass(i.playingClass);f.removeClass(i.pausedClass);f.removeClass(i.progressClass);f.removeClass(i.stoppedClass)}function t(u){return(b)?f.filter('[href="'+u.originalUrl+'"]'):f.eq(u.index)}function l(){var u=g.find("a");return u.length?u:g.children()}if(!b){s=g.children().length<=0?i.template:g.html();n()}else{s=i.template;c();var o=[];a.each(f,function(u,v){o.push({url:encodeURI(a(v).attr("href"))})});j.onLoad(function(){j.setPlaylist(o)});var p=j.getClip(0);if(!p.url&&i.playOnClick){p.update({url:encodeURI(f.eq(0).attr("href"))})}}j.onBegin(function(u){e();t(u).addClass(i.playingClass)});j.onPause(function(u){t(u).removeClass(i.playingClass).addClass(i.pausedClass)});j.onResume(function(u){t(u).removeClass(i.pausedClass).addClass(i.playingClass)});function h(u){j.onBeforeFinish(function(v){t(v).removeClass(i.playingClass);t(v).addClass(i.stoppedClass);if(!v.isInStream&&v.index<f.length-1){return false}else{if(!v.isInStream){this.pause()}}});j.onResume(function(v){if(!v.isInStream&&v.index==f.length-1&&j.getTime()>v.duration-1){j.play(v.index)}})}function r(u){j.onBeforeFinish(function(v){if(!v.isInStream&&v.index>=f.length-1){return false}})}function k(u){j.onFinish(function(v){if(!v.isInStream&&v.index==f.length-1){t(v).removeClass(i.playingClass);t(v).addClass(i.stoppedClass)}})}if(!i.loop&&!i.continuousPlay){h(p)}else{if(i.loop){r(p)}else{k(p)}}j.onUnload(function(){e()});if(!b){j.onPlaylistReplace(function(){n()})}j.onClipAdd(function(v,u){if(s){if(u<f.length){l().eq(u).before(m(v))}else{l().eq(u-1).after(m(v))}}c()});return j})})(jQuery);

/* - collective.flowplayer.js - */
var collective_flowplayer = {
  "params": {
    "src": "http://www.ag.ndsu.edu/++resource++collective.flowplayer/flowplayer.swf"
  }, 
  "config": {
    "clip": {
      "scaling": "fit", 
      "autoBuffering": false, 
      "autoPlay": false
    }, 
    "plugins": {
      "audio": {
        "url": "http%3A//www.ag.ndsu.edu/%2B%2Bresource%2B%2Bcollective.flowplayer/flowplayer.audio.swf"
      }, 
      "controls": {
        "url": "http%3A//www.ag.ndsu.edu/%2B%2Bresource%2B%2Bcollective.flowplayer/flowplayer.controls.swf", 
        "volume": true
      }
    }
  }, 
  "initialVolumePercentage": 50, 
  "loop": false
};

/* - ++resource++collective.flowplayer.js/init.js - */
/*global jQuery, flowplayer, window */
(function($) {
    function initialVolume() {
        var volume = window.collective_flowplayer.initialVolumePercentage;
        if (volume !== null) {
            this.setVolume(volume);
        }
    }

    function loop() {
        return !window.collective_flowplayer.loop;
    }

    initFlowplayer = function(area) {
        if (area === undefined) {
            area = $('body');
        }
        $('.autoFlowPlayer', area).each(function() {
            // Take a copy of the global config
            var config = jQuery.extend(true, {}, window.collective_flowplayer.config);
            var $self = $(this);
            if ($self.is('.minimal')) {
                config.plugins.controls = null;
            }
            var audio = $self.is('.audio');
            if (audio && !$self.is('.minimal')) {
                config.plugins.controls.all = false;
                config.plugins.controls.play = true;
                config.plugins.controls.scrubber = true;
                config.plugins.controls.mute = true;
                config.plugins.controls.volume = true;
                config.plugins.controls.time = true;
                config.plugins.controls.autoHide = false;
            }
            if ($self.is('div')) {
                // comming from Kupu, there are relative urls
                config.clip.baseUrl = $('base').attr('href');
                config.clip.url = $self.find('a').attr('href');
                if (audio) {
                    // force .mp3 extension
                    config.clip.url = config.clip.url + '?e=.mp3';
                }
                // Ignore global autoplay settings
                if ($self.find('img').length === 0) {
                    // no image. Don't autoplay, remove all elements inside the div to show player directly.
                    config.clip.autoPlay = false;
                    $self.empty();
                } else {
                    // Clip is probably linked as image, so autoplay the clip after image is clicked
                    config.clip.autoPlay = true;
                    // If we know there is splash image, we could at least try to match this size
                    $(this).css("width", $self.find('img').width());
                    $(this).css("height", $self.find('img').height());
                }
            }
            flowplayer(this, window.collective_flowplayer.params, config).onLoad(initialVolume).onBeforeFinish(loop);
            $('.flowPlayerMessage').remove();
        });
        $('.playListFlowPlayer').each(function() {
            // Take a copy of the global config
            var config = jQuery.extend(true, {}, window.collective_flowplayer.config);
            var $self = $(this);
            var audio = $self.is('.audio');
            if (audio) {
                config.plugins.controls.fullscreen = false;
            }
            if ($self.is('.minimal')) {
                config.plugins.controls = null;
            }
            if ($self.find('img').length > 0) {
                // has splash
                config.clip.autoPlay = true;
            }
            var portlet_parents = $self.parents('.portlet');
            var playlist_selector = 'div#flowPlaylist';
            var portlet;
            if (portlet_parents.length > 0) {
                portlet = true;
                // playlist has to be bound to unique item
                var playlist_selector_id = portlet_parents.parent().attr('id') + '-playlist';
                $self.parent().find('.flowPlaylist-portlet-marker').attr('id', playlist_selector_id);
                playlist_selector = '#' + playlist_selector_id;
                if (audio && !$self.is('.minimal')) {
                    config.plugins.controls.all = false;
                    config.plugins.controls.play = true;
                    config.plugins.controls.scrubber = true;
                    config.plugins.controls.mute = true;
                    config.plugins.controls.volume = false;
                }
            } else {
                portlet = false;
            }
            if (!portlet) {
                $("#pl").scrollable({
                    items: playlist_selector,
                    size: 4,
                    clickable: false,
                    prev: 'a.prevPage',
                    next: 'a.nextPage'
                });
            }
            // manual = playlist is setup using HTML tags, not using playlist array in config
            flowplayer(this, window.collective_flowplayer.params, config).playlist(playlist_selector, {
                loop: true,
                manual: true
            }).onLoad(initialVolume).onBeforeFinish(loop);
            $self.show();
            $('.flowPlayerMessage').remove();

        });
    };

    $(function() {
        initFlowplayer();
    });
}(jQuery));
