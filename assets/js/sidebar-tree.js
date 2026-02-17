(() => {
  const container = document.querySelector("[data-sidebar-tree]");
  if (!container) return;

  const baseurl = container.getAttribute("data-baseurl") || "";
  const treeUrl = `${baseurl}/assets/tree.json`;

  const createItem = (node) => {
    const li = document.createElement("li");
    li.className = `tree-${node.type}`;

    const title = document.createElement("a");
    title.textContent = node.name;
    if (node.url) {
      title.href = `${baseurl}${node.url}`;
    } else {
      title.href = "#";
      title.className = "tree-disabled";
    }
    li.appendChild(title);

    if (node.type === "dir" && node.children && node.children.length) {
      const ul = document.createElement("ul");
      node.children.forEach((child) => ul.appendChild(createItem(child)));
      li.appendChild(ul);
    }

    return li;
  };

  fetch(treeUrl)
    .then((res) => res.json())
    .then((data) => {
      const ul = document.createElement("ul");
      ul.className = "tree-root";
      if (data && data.children) {
        data.children.forEach((child) => ul.appendChild(createItem(child)));
      }
      container.appendChild(ul);
    })
    .catch(() => {
      container.textContent = "Navigation unavailable.";
    });
})();
