/* Arabic translation layer for the Karrgo site.
 *
 * The pages are rendered by the dc-runtime and re-render on interaction
 * (tab switches, catalogue filters), which would wipe any text we replaced.
 * So rather than translating the source, this swaps strings in the live DOM
 * and re-applies after every render via a MutationObserver.
 *
 * Originals are kept per node, so switching back to English restores the
 * exact source text rather than translating in reverse.
 *
 * Register: Modern Standard Arabic kept deliberately plain, with the
 * Levantine turns of phrase a Lebanese owner actually uses ("كيف منشتغل",
 * "شو بتحتاج"). "يونيفورم" is used rather than "زي موحّد" because that is
 * the word the trade uses here. Numerals stay Western (1, 2, 3) — Lebanon
 * does not use Eastern Arabic-Indic digits in commercial copy.
 */
(function () {
  'use strict';

  var AR = {
    // ---- navigation & chrome ----
    'About': 'من نحن',
    'How we work': 'كيف منشتغل',
    'Products': 'المنتجات',
    'Get a quote': 'اطلب سعر',
    'Chat on WhatsApp': 'تواصل عبر واتساب',
    'WhatsApp': 'واتساب',
    'Message us on WhatsApp': 'راسلنا عبر واتساب',
    'Custom uniforms · Lebanon': 'يونيفورم مخصّص · لبنان',

    // ---- hero (the headline is split across two nodes) ----
    'Uniforms people': 'يونيفورم',
    'want to keep wearing.': 'بيحبّوا يضلّوا لابسينه.',
    "Lebanon's number one uniform provider. Custom workwear for restaurants, hotels, clinics, salons, schools and site crews. Tell us what you need on the sheet below and you get a costed quote back, not a phone tag. Or just message us on WhatsApp and ask.":
      'المزوّد الأول لليونيفورم في لبنان. ملابس عمل مخصّصة للمطاعم والفنادق والعيادات وصالونات التجميل والمدارس وفرق المواقع. خبّرنا شو بتحتاج بالاستمارة تحت ومنرجعلك بسعر مدروس، مش تلفونات ورا بعض. أو ابعتلنا رسالة عالواتساب واسأل.',

    // ---- about ----
    'About us': 'من نحن',
    'What we do': 'شو منعمل',
    'Custom uniforms end to end. Design, fabric, embroidery and print, production, delivery. You approve a physical sample before anything is cut.':
      'يونيفورم مخصّص من الألف للياء. تصميم، قماش، تطريز وطباعة، إنتاج، وتسليم. بتوافق على عيّنة فعلية قبل ما نقصّ شي.',
    'Who we serve': 'مين منخدم',
    'Food and beverage, hospitality, healthcare, beauty, education, security and retail. From a ten-person café to a full hotel floor.':
      'مأكولات ومشروبات، ضيافة، رعاية صحية، تجميل، تعليم، أمن وتجزئة. من كافيه بعشر موظفين لطابق فندق كامل.',
    "How we're different": 'شو بيميّزنا',
    'One point of contact, a written quote, a delivery date we hold to. Your spec stays on file, so a reorder takes one message.':
      'شخص واحد للتواصل، عرض سعر مكتوب، وتاريخ تسليم منلتزم فيه. مواصفاتك بتضل محفوظة عنا، فالطلب التاني بدّو رسالة وحدة.',

    // ---- process ----
    'Consultation': 'استشارة',
    'Quotation': 'عرض سعر',
    'Sample': 'عيّنة',
    'Production': 'إنتاج',
    'Delivery': 'تسليم',

    // ---- quote form ----
    'Quick inquiry': 'طلب سريع',
    'Full spec sheet': 'استمارة مفصّلة',
    'Four fields. Enough for us to come back with a price and the right questions.':
      'أربع خانات. بتكفّي منرجعلك بسعر وبالأسئلة الصح.',
    'Under a minute': 'بأقل من دقيقة',
    'Your name *': 'اسمك *',
    'Business name *': 'اسم المحل *',
    'WhatsApp / phone *': 'واتساب / هاتف *',
    'Email (optional)': 'إيميل (اختياري)',
    'Quantity *': 'الكمية *',
    'Select a range': 'اختر الكمية',
    'Under 10 pieces': 'أقل من 10 قطع',
    '10 to 25 pieces': 'من 10 لـ 25 قطعة',
    '26 to 50 pieces': 'من 26 لـ 50 قطعة',
    '51 to 100 pieces': 'من 51 لـ 100 قطعة',
    '101 to 250 pieces': 'من 101 لـ 250 قطعة',
    '251 to 500 pieces': 'من 251 لـ 500 قطعة',
    'More than 500 pieces': 'أكتر من 500 قطعة',
    'Not sure yet': 'لسا مش متأكد',
    'What you need': 'شو بتحتاج',
    'Select': 'اختر',
    'Shirts': 'قمصان',
    'Hoodies & sweatshirts': 'هوديز وسويت شيرت',
    'Jackets': 'جاكيتات',
    'Chef wear': 'ملابس شيف',
    'Scrubs': 'ملابس طبية',
    'Caps & headwear': 'قبعات وأغطية راس',
    'A full set': 'طقم كامل',
    'Other (specify)': 'غير هيك (حدّد)',
    'Other': 'غير هيك',
    'Anything else': 'شي تاني',
    'Send inquiry': 'ابعت الطلب',
    'Ask on WhatsApp instead': 'اسأل عالواتساب بدل هيك',
    'Rather type than fill a form? Tap the WhatsApp button in the corner.':
      'بتفضّل تكتب بدل ما تعبّي استمارة؟ دوس على زر واتساب بالزاوية.',
    'Who we reply to': 'لمين منرد',
    'Your company': 'اسم شركتك',
    'Colours, logo, sizes, deadline, whatever you already know':
      'ألوان، شعار، قياسات، موعد التسليم، أي شي بتعرفو',

    // ---- products page ----
    'What we make, by trade. Every piece here is customised with your colours and your logo. Pick a category, then send us the ones you want priced.':
      'شو منصنع، حسب القطاع. كل قطعة هون منخصّصها بألوانك وشعارك. اختر فئة وبعدين ابعتلنا القطع يلي بدك سعرها.',
    'Filter': 'تصفية',
    'All': 'الكل',
    'Food & beverage': 'مأكولات ومشروبات',
    'Beauty & wellness': 'تجميل وعناية',
    'Ask price': 'اسأل عن السعر',
    "Don't see it here?": 'ما لقيت يلي بدك؟',
    "This is what we stock and customise most. If you need something else, describe it on the quote sheet or send us a photo on WhatsApp and we'll source it.":
      'هيدا يلي عنا ومنخصّصو أكتر شي. إذا بدك شي تاني، اوصفو بالاستمارة أو ابعتلنا صورة عالواتساب ومنأمّنلك ياه.',

    // ---- messages the component produces conditionally ----
    'Before sending, we still need:': 'قبل ما تبعت، لازم كمان:',
    'your name': 'اسمك',
    'your business name': 'اسم محلك',
    'a WhatsApp or phone number': 'رقم واتساب أو هاتف',
    'a quantity range': 'نطاق الكمية',
    'company name': 'اسم الشركة',
    'at least one garment line with a quantity': 'سطر قطعة واحدة على الأقل مع كمية',
    'what "other" means': 'شو يعني "غير هيك"',
    'Garment by garment. The version you fill in when you know exactly what you want.':
      'قطعة قطعة. النسخة يلي بتعبّيها لما تكون عارف بالضبط شو بدك.',
    'Every field on this sheet reaches us exactly as you write it.':
      'كل خانة بهالاستمارة بتوصلنا متل ما بتكتبها بالضبط.',
    'Copy the spec as text': 'انسخ المواصفات كنص',
    'Copied to clipboard': 'تم النسخ',
    'You added:': 'ضفت:',
    'You did not add any this time. Send them whenever you have them.':
      'ما ضفت ولا وحدة هالمرة. ابعتهن وقت ما يصيروا جاهزين.',
    'None': 'لا شي',
    'To be added': 'رح تنضاف',
    'Other, not specified': 'غير هيك، غير محدّد',
    'Front desk': 'الاستقبال',
    'Floor staff': 'موظفي الصالة',
    'F&B service': 'خدمة مأكولات ومشروبات',
    'Salon / spa': 'صالون / سبا',

    // ---- product names (also used inside the "ask for a price on X" labels) ----
    'Full uniform sets': 'أطقم يونيفورم كاملة',
    'Trousers': 'بناطيل',
    'Polos': 'بولو',
    'T-shirts': 'تي شيرت',
    'Aprons': 'مرايل',
    'Caps': 'قبعات',
    'Name tags': 'بطاقات أسماء',
    'Delivery boxes': 'صناديق توصيل',
    'Branded helmets': 'خوذ مطبوعة',
    'Plastic bags': 'أكياس بلاستيك',
    'Takeaway boxes': 'علب تيك أواي',
    'Placemats': 'مفارش طاولة',
    'Sandwich wraps': 'أوراق ساندويش',
    'Paper cups': 'أكواب ورقية',
    'Napkins': 'مناديل',
    'Coasters': 'قواعد أكواب',
    'Stickers': 'ستيكرز',
    'Full set uniform': 'طقم يونيفورم كامل',
    'Cutting capes': 'مرايل قص',
    'Towels': 'مناشف',
    'Spray bottles': 'بخّاخات'
  };

  // Lowercased product names as they appear inside generated labels.
  var LOWER = {};
  Object.keys(AR).forEach(function (k) { LOWER[k.toLowerCase()] = AR[k]; });

  // Strings the page generates with a number or a product name in them.
  var PATTERNS = [
    [/^(\d+)\s+products?$/i, function (m) { return m[1] + ' منتج'; }],
    [/^(\d+)\s+items?$/i, function (m) { return m[1] + ' قطعة'; }],
    [/^(\d+)\s+photos?$/i, function (m) { return m[1] + ' صور'; }],
    [/^(\d+)\s+pieces?$/i, function (m) { return m[1] + ' قطعة'; }],
    [/^(\d+)\s+lines?$/i, function (m) { return m[1] + ' سطر'; }],
    [/^Ask for a price on (.+)$/i, function (m) {
      var name = LOWER[m[1].toLowerCase()] || m[1];
      return 'اسأل عن سعر ' + name;
    }],
    // "Before sending, we still need:" renders its list of missing fields as
    // a separate text node, so the bare comma-joined list has to match too.
    // The template appends a full stop, which is split off before lookup and
    // restored after. Only translated when every part is known, so it is
    // never half-done.
    [/^[^,]+(,\s*[^,]+)+$/, function (m) {
      var tail = '';
      var core = m[0].replace(/([.!?:])\s*$/, function (_, p) { tail = p; return ''; });
      var parts = core.split(/,\s*/);
      var out = [];
      for (var i = 0; i < parts.length; i++) {
        var k = parts[i].trim();
        var p = AR[k] || LOWER[k.toLowerCase()];
        if (!p) return null;
        out.push(p);
      }
      return out.join('، ') + tail;
    }]
  ];

  function toArabic(s) {
    var t = s.trim();
    if (!t) return null;
    if (Object.prototype.hasOwnProperty.call(AR, t)) return AR[t];
    for (var i = 0; i < PATTERNS.length; i++) {
      var m = t.match(PATTERNS[i][0]);
      if (m) return PATTERNS[i][1](m);
    }
    return null;
  }

  var ATTRS = ['placeholder', 'aria-label', 'title'];
  var SKIP = { SCRIPT: 1, STYLE: 1, NOSCRIPT: 1 };
  // node -> { orig, trans }. Both are kept because the runtime often rewrites
  // a text node's value in place rather than replacing the node: if we only
  // recorded "this node was handled", such a node would keep its new English
  // value forever. Comparing against `trans` tells the two cases apart.
  var state = new WeakMap();
  var attrState = new WeakMap(); // element -> { attr: { orig, trans } }
  var applying = false;
  var lang = 'en';

  function eachTextNode(fn) {
    var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
      acceptNode: function (n) {
        if (!n.parentNode || SKIP[n.parentNode.nodeName]) return NodeFilter.FILTER_REJECT;
        if (n.parentNode.closest && n.parentNode.closest('[data-i18n-skip]')) return NodeFilter.FILTER_REJECT;
        return n.nodeValue.trim() ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT;
      }
    });
    var n, list = [];
    while ((n = walker.nextNode())) list.push(n);
    list.forEach(fn);
  }

  function apply(to) {
    applying = true;
    try {
      eachTextNode(function (node) {
        var st = state.get(node);
        if (to === 'ar') {
          if (st && node.nodeValue === st.trans) return;  // already translated
          var ar = toArabic(node.nodeValue);
          if (ar === null) return;
          var next = node.nodeValue.replace(node.nodeValue.trim(), ar);
          state.set(node, { orig: node.nodeValue, trans: next });
          node.nodeValue = next;
        } else if (st && node.nodeValue === st.trans) {
          node.nodeValue = st.orig;
          state['delete'](node);
        }
      });

      var sel = ATTRS.map(function (a) { return '[' + a + ']'; }).join(',');
      Array.prototype.forEach.call(document.body.querySelectorAll(sel), function (el) {
        ATTRS.forEach(function (a) {
          var cur = el.getAttribute(a);
          if (cur === null) return;
          var store = attrState.get(el) || {};
          var st = store[a];
          if (to === 'ar') {
            if (st && cur === st.trans) return;
            var ar = toArabic(cur);
            if (ar === null) return;
            store[a] = { orig: cur, trans: ar };
            attrState.set(el, store);
            el.setAttribute(a, ar);
          } else if (st && cur === st.trans) {
            el.setAttribute(a, st.orig);
            delete store[a];
            attrState.set(el, store);
          }
        });
      });

      document.documentElement.lang = to;
      document.documentElement.dir = to === 'ar' ? 'rtl' : 'ltr';
      if (btn) btn.textContent = to === 'ar' ? 'EN' : 'عربي';
    } finally {
      applying = false;
    }
  }

  function setLang(to) {
    lang = to;
    try { localStorage.setItem('karrgo-lang', to); } catch (e) {}
    apply(to);
  }

  // ---- the toggle ----
  // Lives inside the sticky nav so it sits with the other controls at the top
  // of the page. The runtime re-renders the nav, so this is re-mounted from
  // the observer whenever it goes missing.
  var btn = null;

  // Delegated on the document rather than bound to the button. The runtime can
  // replace the nav with a copy of itself, and a cloned node does not carry
  // event listeners — such a button would look right and do nothing. Catching
  // the click on the way up means whichever copy is on screen still works.
  document.addEventListener('click', function (e) {
    var t = e.target;
    while (t && t !== document) {
      if (t.id === 'lang-toggle') {
        e.preventDefault();
        setLang(lang === 'ar' ? 'en' : 'ar');
        return;
      }
      t = t.parentNode;
    }
  }, true);

  function mountButton() {
    var host = document.querySelector('nav.nav') || document.body;
    // A re-render can clone the nav along with an already-injected button,
    // leaving a copy that is not our element. Drop any such strays first,
    // otherwise each render adds another toggle.
    Array.prototype.forEach.call(document.querySelectorAll('#lang-toggle'), function (el) {
      if (el !== btn && el.parentNode) el.parentNode.removeChild(el);
    });
    if (btn && btn.parentNode === host) {
      btn.textContent = lang === 'ar' ? 'EN' : 'عربي';
      return;
    }
    if (!btn) {
      btn = document.createElement('button');
      btn.type = 'button';
      btn.id = 'lang-toggle';
      btn.setAttribute('data-i18n-skip', '');
      btn.setAttribute('aria-label', 'Switch language / تغيير اللغة');
    }
    btn.textContent = lang === 'ar' ? 'EN' : 'عربي';
    host.appendChild(btn);
  }

  function boot() {
    try { lang = localStorage.getItem('karrgo-lang') || 'en'; } catch (e) { lang = 'en'; }
    mountButton();
    if (lang === 'ar') apply('ar');

    var pending = false;
    // setTimeout rather than requestAnimationFrame: rAF is throttled or
    // suspended in background tabs and in some embedded contexts, which would
    // leave a re-rendered section stranded in English.
    new MutationObserver(function () {
      if (applying || pending) return;
      pending = true;
      setTimeout(function () {
        pending = false;
        mountButton();
        if (lang === 'ar') apply('ar');
      }, 0);
    }).observe(document.body, { childList: true, subtree: true, characterData: true });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
