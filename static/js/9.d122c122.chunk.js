(this["webpackJsonpreact-ant2"]=this["webpackJsonpreact-ant2"]||[]).push([[9],{535:function(e,t,n){"use strict";n.r(t),n.d(t,"default",(function(){return k}));var a=n(33),r=n.n(a),c=n(88),s=n(52),o=n(45),i=n(0),d=n(37),u=n(35),l=n(48),f=n(516),b=n(234),j=n(400),p=n(162),x=n(543),h=n(553),O=n(554),v=n(515),g=n(6),m=f.a.TabPane;function k(){var e=Object(i.useState)((new Date).toLocaleTimeString()),t=Object(o.a)(e,2),n=(t[0],t[1]),a=Object(i.useState)(1e3)[0],k=Object(i.useState)([!0])[0],w=Object(i.useState)({"lootnika.log":{key:"1",title:"",content:Object(g.jsx)("div",{style:{textAlign:"center",margin:"2em"},children:Object(g.jsx)(b.a,{})}),init:!1,end:-1,offsetEnd:-1,offsetStart:-1,hasMore:!0,loading:!0,records:[]}})[0],y=Object(i.useState)(!0),S=Object(o.a)(y,2),M=S[0],E=S[1],L=Object(i.useState)(!1)[0],T=Object(i.useState)(""),A=Object(o.a)(T,2),D=A[0],C=A[1],I=Object(i.useState)([!1])[0],J=Object(i.useState)([!1])[0],_=Object(i.useState)([""])[0];function B(){return(B=Object(s.a)(r.a.mark((function e(){var t,n,a,s,o,i,f;return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(t=!1,!I[0]){e.next=3;break}return e.abrupt("return",!1);case 3:if(I[0]=!0,!l.b){e.next=10;break}return e.next=7,Object(d.b)("a=log?cmd=list",{status:200,data:u.c},300);case 7:n=e.sent,e.next=13;break;case 10:return e.next=12,Object(d.a)("a=log?cmd=list");case 12:n=e.sent;case 13:if(n){s=Object(c.a)(null===(a=n)||void 0===a?void 0:a.data.files);try{for(s.s();!(o=s.n()).done;)i=o.value,f={key:i,title:i,content:Object(g.jsx)("div",{style:{textAlign:"center",margin:"2em"},children:Object(g.jsx)(b.a,{})}),init:!1,end:-1,offsetEnd:-1,offsetStart:-1,loading:!0,hasMore:!0,records:[]},w[i]=f}catch(r){s.e(r)}finally{s.f()}E(!1),t=!0}return I[0]=!1,e.abrupt("return",t);case 16:case"end":return e.stop()}}),e)})))).apply(this,arguments)}function F(e,t,n,a,r){return N.apply(this,arguments)}function N(){return(N=Object(s.a)(r.a.mark((function e(t,n,a,c,s){var o,i,f,b,j,p,x,h,O,v;return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(o=-1,i=-1,f=[],!l.b){e.next=12;break}return j=u.d[t],c||(j.records=["Fresh random record"]),"user_topics.log"===_[0]&&(j.records=[""]),e.next=9,Object(d.b)("a=log?cmd=read&file=lootnika.log&limit=2&backward=true",{status:200,data:j},600);case 9:b=e.sent,e.next=15;break;case 12:return e.next=14,Object(d.a)("a=log?cmd=read&file=".concat(t,"&limit=").concat(a,"&backward=").concat(c,"&offset=").concat(n));case 14:b=e.sent;case 15:return b&&(o=null===(p=b)||void 0===p?void 0:p.data.offset,i=null===(x=b)||void 0===x?void 0:x.data.end,f=s?c?w[t].records.concat(null===(h=b)||void 0===h?void 0:h.data.records):null===(O=b)||void 0===O?void 0:O.data.records.concat(w.records):null===(v=b)||void 0===v?void 0:v.data.records),e.abrupt("return",[o,i,f]);case 17:case"end":return e.stop()}}),e)})))).apply(this,arguments)}function P(e){return U.apply(this,arguments)}function U(){return(U=Object(s.a)(r.a.mark((function e(t){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.abrupt("return",Object(g.jsx)(v.a,{height:"70vh",dataLength:w[t].records.length,next:function(){return q(!0)},hasMore:w[t].hasMore,loader:Object(g.jsx)("div",{style:{textAlign:"center",margin:"2em"},children:Object(g.jsx)(b.a,{})}),endMessage:Object(g.jsx)("p",{style:{textAlign:"center"},children:Object(g.jsx)("b",{children:"This is top"})}),children:Object(g.jsx)(j.b,{dataSource:w[t].records,renderItem:function(e){return Object(g.jsx)(j.b.Item,{className:"log-list-item",children:Object(g.jsx)("span",{children:e})})}})}));case 1:case"end":return e.stop()}}),e)})))).apply(this,arguments)}function q(e){return z.apply(this,arguments)}function z(){return(z=Object(s.a)(r.a.mark((function e(t){var a,c,s,i,d,u,f,b,j,p,x,h;return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(!t){e.next=19;break}return e.next=3,F(_[0],w[_[0]].offsetStart,50,!0,!1);case 3:return a=e.sent,c=Object(o.a)(a,3),s=c[0],i=c[1],d=c[2],w[_[0]].offsetStart=s,w[_[0]].end=i,u=w[_[0]].records,w[_[0]].records=u.concat(d),e.next=14,P(_[0]);case 14:w[_[0]].content=e.sent,"user_topics.log"===_[0]&&l.b&&(w[_[0]].offsetStart=0),w[_[0]].offsetStart<=0&&(w[_[0]].hasMore=!1),e.next=33;break;case 19:return e.next=21,F(_[0],w[_[0]].offsetEnd,1e3,!1,!1);case 21:return f=e.sent,b=Object(o.a)(f,3),j=b[0],p=b[1],x=b[2],w[_[0]].offsetEnd=j,w[_[0]].end=p,h=w[_[0]].records,w[_[0]].records=x.reverse().concat(h),e.next=32,P(_[0]);case 32:w[_[0]].content=e.sent;case 33:n((new Date).toLocaleTimeString());case 34:case"end":return e.stop()}}),e)})))).apply(this,arguments)}function G(e,t){return H.apply(this,arguments)}function H(){return(H=Object(s.a)(r.a.mark((function e(t,a){var c,s,o,i,f,b;return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(l.b?C("/lootnika/static/files/"+t):C(l.a+"/a=log?cmd=get&file="+t),!J[0]){e.next=3;break}return e.abrupt("return",!1);case 3:if(J[0]=!0,!l.b){e.next=12;break}return(s=u.d[t]).records=s.records.reverse(),e.next=9,Object(d.b)("a=log?cmd=read&file=lootnika.log&limit=2&backward=true",{status:200,data:s},600);case 9:c=e.sent,e.next=15;break;case 12:return e.next=14,Object(d.a)("a=log?cmd=read&file=".concat(t,"&limit=").concat(a,"&backward=true"));case 14:c=e.sent;case 15:return c&&(w[t].records=null===(o=c)||void 0===o?void 0:o.data.records,w[t].end=null===(i=c)||void 0===i?void 0:i.data.end,w[t].offsetEnd=null===(f=c)||void 0===f?void 0:f.data.end,w[t].offsetStart=null===(b=c)||void 0===b?void 0:b.data.offset,w[t].hasMore=!0,_[0]=t),w[t].init=!0,e.next=19,P(t);case 19:w[t].content=e.sent,J[0]=!1,n((new Date).toLocaleTimeString());case 22:case"end":return e.stop()}}),e)})))).apply(this,arguments)}function K(){return(K=Object(s.a)(r.a.mark((function e(t){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:w[t].init?(l.b?C("/lootnika/static/files/"+t):C(l.a+"/a=log?cmd=get&file="+t),_[0]=t):G(t,50);case 1:case"end":return e.stop()}}),e)})))).apply(this,arguments)}Object(d.e)((function(){M&&!I[0]&&function(){return B.apply(this,arguments)}()&&G("lootnika.log",50),M||I[0]||(k[0]=!1)}),k[0]?a:null);var Q=Object(g.jsxs)("div",{children:[Object(g.jsx)(p.a,{loading:L,onClick:function(){return q(!1)},icon:Object(g.jsx)(h.a,{}),children:"Update"}),Object(g.jsx)(p.a,{loading:L,href:D,icon:Object(g.jsx)(O.a,{}),children:"Download"})]});return Object(g.jsx)(x.a,{title:"Logs viewer",children:Object(g.jsx)(f.a,{type:"card",onChange:function(e){return K.apply(this,arguments)},tabBarExtraContent:Q,children:Object.values(w).map((function(e){return Object(g.jsx)(m,{tab:e.title,children:e.content},e.key)}))})})}}}]);
//# sourceMappingURL=9.d122c122.chunk.js.map