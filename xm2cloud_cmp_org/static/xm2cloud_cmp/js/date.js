// for parse date or datetime
/*
* 1. can not parse datatime with no second filed now ...
*
* parseDate('2006-1-1') return new Date(2006,0,1)
* parseDate(' 2006-1-1 ') return new Date(2006,0,1)
* parseDate('2006-1-1 15:14:16') return new Date(2006,0,1,15,14,16)
* parseDate(' 2006-1-1 15:14:16 ') return new Date(2006,0,1,15,14,16);
* parseDate('2006-1-1 15:14:16.254') return new Date(2006,0,1,15,14,16,254)
* parseDate(' 2006-1-1 15:14:16.254 ') return new Date(2006,0,1,15,14,16,254)
* parseDate('不正确的格式') retrun null
*
* */
function parse_date(str){
  if(typeof str == 'string'){
    var results = str.match(/^ *(\d{4})-(\d{1,2})-(\d{1,2}) *$/);
    if(results && results.length>3)
      return new Date(parseInt(results[1]),parseInt(results[2]) -1,parseInt(results[3]));
    results = str.match(/^ *(\d{4})-(\d{1,2})-(\d{1,2}) +(\d{1,2}):(\d{1,2}):(\d{1,2}) *$/);
    if(results && results.length>6)
      return new Date(parseInt(results[1]),parseInt(results[2]) -1,parseInt(results[3]),parseInt(results[4]),parseInt(results[5]),parseInt(results[6]));
    results = str.match(/^ *(\d{4})-(\d{1,2})-(\d{1,2}) +(\d{1,2}):(\d{1,2}):(\d{1,2})\.(\d{1,9}) *$/);
    if(results && results.length>7)
      return new Date(parseInt(results[1]),parseInt(results[2]) -1,parseInt(results[3]),parseInt(results[4]),parseInt(results[5]),parseInt(results[6]),parseInt(results[7]));
  }
  return null;
}


// for convert new Date to metric form and util datetime
/*
*
* &from=04:00_20110501&until=16:00_20110501
*
* */
function to_metrictime(dt) {
    if(typeof dt == 'string') dt = parse_date(dt);
     if(dt instanceof Date) {
         var y = dt.getFullYear();
         var m = dt.getMonth() + 1;
         var d = dt.getDate();
         var h = dt.getHours();
         var i = dt.getMinutes();

         return (h<10?'0':'')+h+':'+(i<10?'0':'')+i+'_'+(y<10?'0':'')+y+(m<10?'0':'')+m+(d<10?'0':'')+d;
     }else{
         return '';
    }
}


// for convert timestamp to time format
/**
 *
 *  1515339180000 - 02:33
 *
 */
function to_strtime(ts) {
    var d = new Date(ts);
    var hh = d.getHours()
        ,ii = d.getMinutes();
    return (hh<10?'0':'')+hh+':'+(ii<10?'0':'')+ii;
}


// for convert timestamp to date format
/**
 *
 *  1515339180000 - 2018-01-08
 *
 */
function to_strdate(ts) {
    var d = new Date(ts);
    var yyyy = d.getFullYear()
        ,mm = d.getMonth() + 1
        ,dd = d.getDate();
    return yyyy+'-'+(mm<10?'0':'')+mm+'-'+(dd<10?'0':'')+dd;
}


// for convert timestamp to datetime format
/**
 *
 *  1515339180000 - 2018-01-08 02:33
 *
 */
function to_strdatetime(ts) {
    return to_strdate(ts)+' '+to_strtime(ts);
}
