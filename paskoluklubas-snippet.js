(() => {
    const trs = [...document.querySelectorAll("body > div.site-main > div:nth-child(2) > div.tabbed-sections.tabbed-style1 > div.content-view.activated > div.tabbed-sections.tabbed-style3 > section.activated > div > div > table > tbody > tr:not(.remainder):not(.expandable-row)")];
    const events = trs.map(el => {
        const tds = el.querySelectorAll("td");
        return {
            date: tds[0].querySelector("span").textContent.trim(),
            name: tds[1].querySelector("span").textContent.trim(),
            debit: tds[2].querySelector("span").textContent.trim(),
            credit: tds[3].querySelector("span").textContent.trim()
        }
    });
    copy(JSON.stringify(events, null, 2) + "\n");
})();
