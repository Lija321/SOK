  let isGraphLoaded = false;
  const configuration = { attributes: true, childList: true, subtree: true };

  const graphObserver = new MutationObserver(() => {
    if (!isGraphLoaded) {
      renderNewBirdView();
    }
  });
  window.onload = () => {
    const mainCanvas = document.querySelector("#main-canvas svg");
    if (mainCanvas) {
      graphObserver.observe(mainCanvas, configuration);
    }
  };



  function renderNewBirdView() {
    isGraphLoaded = true;

    const mainSvg = d3.select("#main-canvas svg");
    const mainSvgHtml = mainSvg.html();

    d3.select("#bird-content").selectAll("*").remove();

    const birdViewSvg = d3.select("#bird-content")
      .append("svg")
      .attr("width", "100%")
      .attr("height", "100%")
      .attr("id", "bird-view-svg");

    const gContentWrapper = birdViewSvg.append("g")
      .attr("id", "bird-content-wrapper")
      .html(mainSvgHtml);

    const bBox = gContentWrapper.node().getBBox();
    const birdWidth = birdViewSvg.node().clientWidth;
    const birdHeight = birdViewSvg.node().clientHeight;

    const xScale = birdWidth / bBox.width;
    const yScale = birdHeight / bBox.height;
    const minScale = Math.min(xScale, yScale);
    const maxScale = Math.max(xScale,yScale);

    const translateX = (birdWidth / 2) - (bBox.width * minScale / 2) - (bBox.x * minScale);
    const translateY = (birdHeight / 2) - (bBox.height * minScale / 2) - (bBox.y * minScale);

    gContentWrapper.attr("transform", `translate(${translateX},${translateY}) scale(${minScale})`);
    const mainCanvas = document.getElementById("main-canvas");
    const mainViewWidth = mainCanvas.clientWidth;
    const mainViewHeight = mainCanvas.clientHeight;

    // Convert visible size to bird-view coordinates
    const rectWidth = mainViewWidth * minScale;
    const rectHeight = mainViewHeight * minScale;
    //VIEWPORT
    birdViewSvg.append("rect")
      .attr("x", translateX)
      .attr("y", translateY)
      .attr("width", rectWidth)
      .attr("height", rectHeight)
      .attr("fill", "none")
      .attr("stroke", "red")
      .attr("stroke-width", 2)
      .attr("id", "bird-view-border");

    // OPT
    birdViewSvg.selectAll("g.node[click-focus='true']").on("click", function () {
      const id = d3.select(this).attr("id");
      dispatchNodeFocusEvent(id);
    });

    // RES FLAG
    setTimeout(() => { isGraphLoaded = false; }, 100);
  }

  function dispatchNodeFocusEvent(nodeId) {
    const event = new CustomEvent("birdViewNodeFocus", { detail: { id: nodeId } });
    window.dispatchEvent(event);
  }