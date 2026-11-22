/// <reference path="/var/www/pocketbase/pb_data/types.d.ts" />

/**
 * Automatically dispatches lead notifications whenever a visitor submits
 * any form or callback number into 'teklif_talepleri'.
 */
onRecordAfterCreateSuccess((e) => {
  try {
    var lib = require(__hooks + "/lead_notify_lib.js");
    var r = e.record;
    var lead = {
      id: r.id,
      fullName: r.getString("fullName"),
      phone: r.getString("phone"),
      serviceType: r.getString("serviceType"),
      buildingUnits: r.getString("buildingUnits"),
      message: r.getString("message"),
      channel: r.getString("channel"),
      landingPage: r.getString("landingPage"),
      utmSource: r.getString("utmSource"),
      utmCampaign: r.getString("utmCampaign"),
      utmTerm: r.getString("utmTerm"),
      gclid: r.getString("gclid"),
      fbclid: r.getString("fbclid"),
    };
    var res = lib.dispatchNotifications($app, lead, {
      isTest: false,
      MailerMessage: MailerMessage,
      http: $http,
    });
    console.log(
      "[lead_notify] lead=" + r.id +
      " skipped=" + res.skipped +
      " emailSent=" + res.emailSent +
      (res.emailError ? " emailErr=" + res.emailError : "") +
      " ntfySent=" + res.ntfySent +
      " tgSent=" + res.telegramSent
    );
  } catch (err) {
    console.log("[lead_notify] ERROR:", err);
  }
  e.next();
}, "teklif_talepleri");

/**
 * Superuser-only test endpoint used by /merkez "Test Bildirimi Gönder".
 */
routerAdd("POST", "/api/celebi/test-notify", (e) => {
  var lib = require(__hooks + "/lead_notify_lib.js");
  var sampleLead = {
    fullName: "Test Müşteri (Yönetim Merkezi)",
    phone: "0535 000 00 00",
    serviceType: "Site & Apartman Yönetimi",
    buildingUnits: "24 Daire",
    message: "Bu mesaj /merkez bildirim ayarlarınızı doğrulamak için gönderilen bir testtir.",
    channel: "Yönetim Merkezi Test Bildirimi",
    landingPage: "/merkez",
    utmSource: "admin_test",
    utmCampaign: "",
    utmTerm: "",
    gclid: "",
    fbclid: "",
  };
  var res = lib.dispatchNotifications($app, sampleLead, {
    isTest: true,
    MailerMessage: MailerMessage,
    http: $http,
  });
  return e.json(200, res);
}, $apis.requireSuperuserAuth());
