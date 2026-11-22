/**
 * Shared notification helper library for PocketBase pb_hooks.
 * Loaded inside hook handlers via require(__hooks + "/lead_notify_lib.js").
 */

function escapeHtml(val) {
  return String(val == null ? "" : val)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function toAsciiHeader(str) {
  var map = {
    "ç": "c", "Ç": "C",
    "ğ": "g", "Ğ": "G",
    "ı": "i", "İ": "I",
    "ö": "o", "Ö": "O",
    "ş": "s", "Ş": "S",
    "ü": "u", "Ü": "U",
  };
  return String(str || "").replace(/[çÇğĞıİöÖşŞüÜ]/g, function (ch) {
    return map[ch] || ch;
  });
}

function parseEmails(rawStr) {
  var parts = String(rawStr || "").split(/[,;\s]+/);
  var seen = {};
  var result = [];
  for (var i = 0; i < parts.length; i++) {
    var em = parts[i].trim().toLowerCase();
    if (!em) continue;
    var atIdx = em.indexOf("@");
    var dotIdx = atIdx > 0 ? em.indexOf(".", atIdx + 1) : -1;
    if (atIdx > 0 && dotIdx > atIdx + 1 && dotIdx < em.length - 1 && !seen[em]) {
      seen[em] = true;
      result.push(em);
    }
  }
  return result;
}

function formatPhoneForLinks(rawPhone) {
  var raw = String(rawPhone || "").trim();
  var digits = raw.replace(/[^0-9]/g, "");
  var waDigits = "";
  if (digits.indexOf("90") === 0 && digits.length >= 12) {
    waDigits = digits;
  } else if (digits.indexOf("0") === 0 && digits.length >= 11) {
    waDigits = "9" + digits;
  } else if (digits.length === 10) {
    waDigits = "90" + digits;
  } else if (digits.length > 0) {
    waDigits = digits;
  }
  var telHref = waDigits ? "tel:+" + waDigits : "tel:+903222351588";
  var waUrl = waDigits ? "https://wa.me/" + waDigits : "https://wa.me/905358730324";
  return { raw: raw, digits: waDigits, telHref: telHref, waUrl: waUrl };
}

function loadNotificationConfig($app) {
  try {
    var items = $app.findRecordsByFilter("bildirim_ayarlari", "id != ''", "", 1, 0);
    if (items && items.length > 0) {
      return items[0];
    }
  } catch (err) {
    console.log("[lead_notify] bildirim_ayarlari okunamadi:", err);
  }
  return null;
}

function buildLeadEmailHtml(lead) {
  var links = formatPhoneForLinks(lead.phone);
  var fullName = escapeHtml(lead.fullName || "Ziyaretçi");
  var phone = escapeHtml(lead.phone || "-");
  var serviceType = escapeHtml(lead.serviceType || "Site & Apartman Yönetimi");
  var buildingUnits = escapeHtml(lead.buildingUnits || "-");
  var message = escapeHtml(lead.message || "-");
  var channel = escapeHtml(lead.channel || "Web Sitesi");
  var landingPage = escapeHtml(lead.landingPage || "/");

  var utmParts = [];
  if (lead.gclid) utmParts.push("Google Ads (gclid)");
  if (lead.fbclid) utmParts.push("Meta Ads (fbclid)");
  if (lead.utmSource) utmParts.push("Kaynak: " + lead.utmSource);
  if (lead.utmCampaign) utmParts.push("Kampanya: " + lead.utmCampaign);
  if (lead.utmTerm) utmParts.push("Kelime: " + lead.utmTerm);
  var attrText = escapeHtml(utmParts.length ? utmParts.join(" • ") : "Doğrudan / Organik Ziyaret");

  return (
    '<!doctype html><html lang="tr"><body style="margin:0;padding:24px;background:#f1f5f9;font-family:Arial,Helvetica,sans-serif;color:#0f172a;">' +
    '<div style="max-width:600px;margin:0 auto;background:#ffffff;border-radius:20px;border:1px solid #e2e8f0;overflow:hidden;">' +
    '<div style="background:linear-gradient(135deg,#0f172a,#004AAD);padding:24px 28px;color:#ffffff;">' +
    '<div style="font-size:12px;font-weight:bold;letter-spacing:1px;text-transform:uppercase;color:#38bdf8;margin-bottom:6px;">ÇELEBİ YÖNETİM &amp; TEMİZLİK • CANLI TALEP</div>' +
    '<h1 style="margin:0;font-size:22px;line-height:1.3;">🔔 ' + channel + '</h1>' +
    '</div>' +
    '<div style="padding:24px 28px;">' +
    '<div style="background:#f8fafc;border:1px solid #cbd5e1;border-radius:14px;padding:18px;margin-bottom:20px;text-align:center;">' +
    '<div style="font-size:12px;color:#475569;font-weight:bold;margin-bottom:6px;">MÜŞTERİ TELEFON NUMARASI</div>' +
    '<div style="font-size:26px;font-weight:800;color:#0f172a;letter-spacing:0.5px;margin-bottom:16px;">' + phone + '</div>' +
    '<a href="' + links.telHref + '" style="display:inline-block;padding:12px 22px;margin:4px;border-radius:12px;background:#0f172a;color:#ffffff;text-decoration:none;font-weight:bold;font-size:14px;">📞 HEMEN ARA</a>' +
    '<a href="' + links.waUrl + '" style="display:inline-block;padding:12px 22px;margin:4px;border-radius:12px;background:#059669;color:#ffffff;text-decoration:none;font-weight:bold;font-size:14px;">💬 WHATSAPP&#39;TAN YAZ</a>' +
    '</div>' +
    '<table style="width:100%;border-collapse:collapse;font-size:14px;">' +
    '<tr><td style="padding:10px 8px;border-bottom:1px solid #e2e8f0;color:#64748b;width:140px;"><strong>Ad Soyad:</strong></td><td style="padding:10px 8px;border-bottom:1px solid #e2e8f0;font-weight:bold;">' + fullName + '</td></tr>' +
    '<tr><td style="padding:10px 8px;border-bottom:1px solid #e2e8f0;color:#64748b;"><strong>Hizmet:</strong></td><td style="padding:10px 8px;border-bottom:1px solid #e2e8f0;">' + serviceType + '</td></tr>' +
    '<tr><td style="padding:10px 8px;border-bottom:1px solid #e2e8f0;color:#64748b;"><strong>Birim / Alan:</strong></td><td style="padding:10px 8px;border-bottom:1px solid #e2e8f0;">' + buildingUnits + '</td></tr>' +
    '<tr><td style="padding:10px 8px;border-bottom:1px solid #e2e8f0;color:#64748b;"><strong>Mesaj / Not:</strong></td><td style="padding:10px 8px;border-bottom:1px solid #e2e8f0;">' + message + '</td></tr>' +
    '<tr><td style="padding:10px 8px;border-bottom:1px solid #e2e8f0;color:#64748b;"><strong>Sayfa:</strong></td><td style="padding:10px 8px;border-bottom:1px solid #e2e8f0;font-family:monospace;">' + landingPage + '</td></tr>' +
    '<tr><td style="padding:10px 8px;color:#64748b;"><strong>Kaynak:</strong></td><td style="padding:10px 8px;">' + attrText + '</td></tr>' +
    '</table>' +
    '<div style="margin-top:22px;padding-top:16px;border-top:1px solid #e2e8f0;text-align:center;font-size:12px;color:#64748b;">' +
    'Tüm talepleri yönetmek için <a href="https://celebiyonetim.com.tr/merkez" style="color:#004AAD;font-weight:bold;">Yönetim Merkezi (/merkez)</a> panelini açabilirsiniz.' +
    '</div></div></div></body></html>'
  );
}

function dispatchNotifications($app, lead, opts) {
  var options = opts || {};
  var isTest = options.isTest === true;
  var cfg = loadNotificationConfig($app);

  var result = {
    ok: true,
    skipped: false,
    emailSent: false,
    emailError: "",
    ntfySent: false,
    ntfyError: "",
    telegramSent: false,
    telegramError: "",
  };

  if (!isTest && (!cfg || !cfg.getBool("aktif"))) {
    result.skipped = true;
    return result;
  }

  var emails = cfg ? parseEmails(cfg.getString("aliciMailler")) : [];
  var ntfyTopic = cfg ? String(cfg.getString("ntfyTopic") || "").trim() : "";
  var tgToken = cfg ? String(cfg.getString("telegramBotToken") || "").trim() : "";
  var tgChatId = cfg ? String(cfg.getString("telegramChatId") || "").trim() : "";

  var links = formatPhoneForLinks(lead.phone);
  var prefix = isTest ? "[TEST] " : "";
  var subject = prefix + "Yeni Talep: " + (lead.phone || "-") + " (" + (lead.serviceType || "Site Yönetimi") + ")";

  // 1. E-posta kanalı
  var MailerCtor = options.MailerMessage || MailerMessage;
  var settings = $app.settings();
  var smtp = settings ? settings.smtp : null;
  var meta = settings ? settings.meta : null;

  if (emails.length === 0) {
    result.emailError = "Bildirim alınacak e-posta adresi girilmemiş.";
  } else if (!smtp || !smtp.enabled || !smtp.host || smtp.host === "smtp.example.com") {
    result.emailError = "SMTP gönderici ayarları henüz aktif değil.";
  } else {
    try {
      var fromAddr = (meta && meta.senderAddress && meta.senderAddress !== "support@example.com")
        ? meta.senderAddress
        : smtp.username;
      var toList = [];
      for (var i = 0; i < emails.length; i++) {
        toList.push({ address: emails[i] });
      }
      var mailMsg = new MailerCtor({
        from: {
          address: fromAddr || "noreply@celebiyonetim.com.tr",
          name: "Çelebi Yönetim Web Bildirim",
        },
        to: toList,
        subject: subject,
        html: buildLeadEmailHtml(lead),
      });
      $app.newMailClient().send(mailMsg);
      result.emailSent = true;
    } catch (err) {
      result.emailError = String(err);
    }
  }

  var httpClient = options.http || $http;

  // 2. Opsiyonel ntfy.sh anlık push kanalı
  if (ntfyTopic) {
    try {
      var ntfyBody =
        (isTest ? "[TEST BİLDİRİMİ]\n" : "") +
        "Ad: " + (lead.fullName || "Ziyaretçi") + "\n" +
        "Tel: " + (lead.phone || "-") + "\n" +
        "Hizmet: " + (lead.serviceType || "-") + "\n" +
        "Sayfa: " + (lead.landingPage || "/") + "\n" +
        "WhatsApp: " + links.waUrl;
      var ntfyRes = httpClient.send({
        method: "POST",
        url: "https://ntfy.sh/" + encodeURIComponent(ntfyTopic),
        body: ntfyBody,
        headers: {
          "Title": toAsciiHeader(subject),
          "Priority": "urgent",
          "Click": links.waUrl,
          "Tags": "phone,bell",
        },
        timeout: 10,
      });
      if (ntfyRes.statusCode >= 200 && ntfyRes.statusCode < 300) {
        result.ntfySent = true;
      } else {
        result.ntfyError = "HTTP " + ntfyRes.statusCode;
      }
    } catch (err) {
      result.ntfyError = String(err);
    }
  }

  // 3. Opsiyonel Telegram kanalı
  if (tgToken && tgChatId) {
    try {
      var tgText =
        "🔔 <b>" + escapeHtml(prefix + (lead.channel || "Yeni Web Talebi")) + "</b>\n" +
        "👤 <b>Ad:</b> " + escapeHtml(lead.fullName || "Ziyaretçi") + "\n" +
        "📱 <b>Telefon:</b> <code>" + escapeHtml(lead.phone || "-") + "</code>\n" +
        "🏢 <b>Hizmet:</b> " + escapeHtml(lead.serviceType || "-") + "\n" +
        "📄 <b>Sayfa:</b> " + escapeHtml(lead.landingPage || "/") + "\n" +
        (lead.message ? "💬 <b>Not:</b> " + escapeHtml(lead.message) + "\n" : "") +
        "\n👉 <a href=\"" + links.waUrl + "\">WhatsApp&#39;tan Yaz</a> | " + escapeHtml(links.telHref);
      var tgRes = httpClient.send({
        method: "POST",
        url: "https://api.telegram.org/bot" + encodeURIComponent(tgToken) + "/sendMessage",
        body: JSON.stringify({
          chat_id: tgChatId,
          text: tgText,
          parse_mode: "HTML",
          disable_web_page_preview: true,
        }),
        headers: { "Content-Type": "application/json" },
        timeout: 10,
      });
      if (tgRes.statusCode >= 200 && tgRes.statusCode < 300) {
        result.telegramSent = true;
      } else {
        result.telegramError = "HTTP " + tgRes.statusCode;
      }
    } catch (err) {
      result.telegramError = String(err);
    }
  }

  return result;
}

module.exports = {
  loadNotificationConfig: loadNotificationConfig,
  parseEmails: parseEmails,
  formatPhoneForLinks: formatPhoneForLinks,
  buildLeadEmailHtml: buildLeadEmailHtml,
  dispatchNotifications: dispatchNotifications,
};
