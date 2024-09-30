const initTabs = () => {
    const tabNodes = document.querySelectorAll('.tabs');
    for (const node of tabNodes) {
        // bind events to toggle tabs for each component occurrence
        for (const tabBtn of node.querySelectorAll('.tabs__item')) {
            tabBtn.addEventListener('click', event => {
                // ignore if it's already active
                if (tabBtn.classList.contains('.tabs__item--active')) {
                    return;
                }

                // otherwise, remove the active class from the active button and pane
                node.querySelector('.tabs__item--active').classList.remove('tabs__item--active');
                node.querySelector('.tabs__pane--active').classList.remove('tabs__pane--active');

                // and activate the target
                tabBtn.classList.add('tabs__item--active');
                const id = tabBtn.dataset.id;
                const tabPane = document.getElementById(id);
                tabPane.classList.add("tabs__pane--active");
            });
        }
    }
};

export default initTabs;
