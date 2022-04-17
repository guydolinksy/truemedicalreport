// Original JavaScript code by Chirp Internet: chirpinternet.eu
// Please acknowledge use of this code by including this header.

export function Highlighter(id, tag) {
    let targetNode = document.getElementById(id) || document.body;
    let highlightTag = tag || "MARK";
    let skipTags = new RegExp("^(?:" + highlightTag + "|SCRIPT|FORM)$");
    let colors = ["#ffff66"];
    let wordColor = [];
    let colorIdx = 0;
    let matchRegExp = "";

    this.setRegex = function (input) {
        matchRegExp = new RegExp(`(${input})`, "i");
    };

    // recursively apply word highlighting
    this.highlightWords = function (node) {
        if (node === undefined || !node) return;
        if (!matchRegExp) return;
        if (skipTags.test(node.nodeName)) return;

        if (node.hasChildNodes()) {
            for (let i = 0; i < node.childNodes.length; i++)
                this.highlightWords(node.childNodes[i]);
        }
        if (node.nodeType === 3) { // NODE_TEXT

            let nv, regs;

            if ((nv = node.nodeValue) && (regs = matchRegExp.exec(nv))) {

                if (!wordColor[regs[0].toLowerCase()]) {
                    wordColor[regs[0].toLowerCase()] = colors[colorIdx++ % colors.length];
                }

                let match = document.createElement(highlightTag);
                match.appendChild(document.createTextNode(regs[0]));
                match.style.backgroundColor = wordColor[regs[0].toLowerCase()];
                match.style.color = "#000";

                let after = node.splitText(regs.index);
                after.nodeValue = after.nodeValue.substring(regs[0].length);
                node.parentNode.insertBefore(match, after);

            }
        }
    };

    // remove highlighting
    this.remove = function () {
        let arr = document.getElementsByTagName(highlightTag), el;
        while (arr.length && (el = arr[0])) {
            let parent = el.parentNode;
            parent.replaceChild(el.firstChild, el);
            parent.normalize();
        }
    };

    // start highlighting at target node
    this.apply = function (input) {
        this.remove();
        if (input) {
            this.setRegex(input.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'));
            this.highlightWords(targetNode);
        }
    };

}