<nav>
% for item in menu:
    <a href="${item['url']}" title="${item['title']}" >${item['label']}</a> |
% end for
</nav>
