document.getElementById("cancelButton").disabled = true;

var firstColor = "rgb(0, 132, 180)"
var secondColor = "rgb(255, 153, 0)"
var serverName = "http://boffa.top/Italian-politicians-tweets-visualization"
//var serverName = "http://0.0.0.0:8000"

function readMore() {
    var dots = document.getElementById("dots");
    var moreText = document.getElementById("more");
    var btnText = document.getElementById("myBtn");

    if (dots.style.display === "none") {
        dots.style.display = "inline";
        btnText.innerHTML = "Read more";
        moreText.style.display = "none";
    } else {
        dots.style.display = "none";
        btnText.innerHTML = "Read less";
        moreText.style.display = "inline";
    }
}

function cleanTwitterEnbeddedTweets() {
    document.getElementById("leftTweetsPoliticianContainer").innerHTML = "";
    document.getElementById("rightTweetsPoliticianContainer").innerHTML = "";
}

function cleanTwitterEnbeddedProfiles() {
    document.getElementById("leftProfilePoliticianContainer").innerHTML = "";
    document.getElementById("rightProfilePoliticianContainer").innerHTML = "";
}

function addClipPath(imageRadius) {
    var svgElement = document.getElementById("svg")
    svgElement.innerHTML = "<clipPath id='clipCircle'> <circle r=" + imageRadius + " cx=" + imageRadius / 2 + " cy=" + imageRadius / 2 + " /> </clipPath>"
}

function fromWidthCardToImageRadius(widthCard) {
    return widthCard / 20;
}
function sumRatiosPolitician(d, name1, name2) {
    var sum = (parseFloat(d.politicians[name1]["ratio"]) + parseFloat(d.politicians[name2]["ratio"]));
    return sum;
}

function fromSumToSize(sum) {
    return sum * 2500 + 15
}
// First, load the widgets.js file asynchronously
window.twttr = (function (d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0],
        t = window.twttr || {};
    if (d.getElementById(id)) return;
    js = d.createElement(s);
    js.id = id;
    js.src = "https://platform.twitter.com/widgets.js";
    fjs.parentNode.insertBefore(js, fjs);

    t._e = [];
    t.ready = function (f) {
        t._e.push(f);
    };

    return t;
}(document, "script", "twitter-wjs"));

fetch(serverName + "/d3/politicians.json")
    .then(function (response) {
        return response.json();
    })
    .then(function (objectPoliticians) {
        var index = 0;
        var firstPoliticiansSelect = document.getElementById("firstPoliticiansSelect");
        var secondPoliticiansSelect = document.getElementById("secondPoliticiansSelect");
        for (var key in objectPoliticians) {
            var opt1 = document.createElement("option");
            var opt2 = document.createElement("option");
            opt1.value = index;
            opt1.innerHTML = key;
            opt2.value = index;
            opt2.innerHTML = key;
            // then append it to the select element
            firstPoliticiansSelect.appendChild(opt1);
            secondPoliticiansSelect.appendChild(opt2);
            index++;
        }

        var primaryButton = document.getElementById("primaryButton");
        primaryButton.onclick = function () {
            var firstSelected = firstPoliticiansSelect.options[firstPoliticiansSelect.selectedIndex].text;
            var secondSelected = secondPoliticiansSelect.options[secondPoliticiansSelect.selectedIndex].text;
            if (firstSelected != "--" && firstSelected != "--") {
                firstPoliticiansSelect.classList.remove("is-invalid");
                secondPoliticiansSelect.classList.remove("is-invalid");
                document.getElementById("card").classList.remove("d-none");
                var widthCard = document.getElementById("card").clientWidth - 30;
                var heightCard = window.innerHeight * 0.6;
                var imageRadius = fromWidthCardToImageRadius(widthCard);
                var xOffSet = imageRadius * 1.9;

                addClipPath(imageRadius);
                var svg = document.getElementById('svg');
                svg.setAttribute("width", widthCard);
                svg.setAttribute("height", heightCard);

                //create somewhere to put the force directed graph
                var svg = d3.select("svg"),
                    width = +svg.attr("width"),
                    height = +svg.attr("height");

                d3.json(serverName + "/d3/TopicRatiosForPoliticians.json").then(function (graph) {
                    //set up the simulation and add forces

                    graph.nodes.push(
                        {
                            "id": firstSelected,
                            "color": objectPoliticians[firstSelected]["color"],
                            "isTopic": 0,
                            "side": "left"
                        }
                    );

                    graph.nodes.push(
                        {
                            "id": secondSelected,
                            "color": objectPoliticians[secondSelected]["color"],
                            "isTopic": 0,
                            "side": "right"
                        }
                    );

                    var simulation = d3.forceSimulation(graph.nodes)
                    simulation
                        .alpha(0.2)
                        .force("charge", d3.forceManyBody().strength(-3000))
                        .force('collision', d3.forceCollide().radius(function (d) {
                            if (d.isTopic == 1) {
                                return fromSumToSize(sumRatiosPolitician(d, firstSelected, secondSelected));
                            }
                            else {
                                return imageRadius;
                            }
                        })
                            .strength(1)
                            .iterations(3))
                        .force("xCenter", d3.forceX().x(widthCard / 2).strength(function (d) {
                            if (d.isTopic == 1) {
                                return sumRatiosPolitician(d, firstSelected, secondSelected) * 35 + 0.25;
                            }
                            else {
                                return 0;
                            }
                        }))
                        .force("yCenter", d3.forceY().y(heightCard / 2).strength(function (d) {
                            if (d.isTopic == 1) {
                                return sumRatiosPolitician(d, firstSelected, secondSelected) * 35 + 0.45;
                            }
                            else {
                                return 1;
                            }
                        }))

                        .force('xLeft', d3.forceX()
                            .x(xOffSet).strength(function (d) {
                                if (d.isTopic == 1) {
                                    return (d.politicians[firstSelected]["ratio"] * 100);
                                }
                                else {
                                    if (d.side == "left") {
                                        return 1;
                                    }
                                    else {
                                        return 0;
                                    }
                                }
                            }))
                        .force('xRigth', d3.forceX()
                            .x(width - xOffSet - imageRadius).strength(function (d) {
                                if (d.isTopic == 1) {
                                    return (d.politicians[secondSelected]["ratio"] * 100);
                                }
                                else {
                                    if (d.side == "left") {
                                        return 0;
                                    }
                                    else {
                                        return 1;
                                    }
                                }
                            }))

                    //add tick instructions:
                    simulation.on("tick", tickActions);
                    //add encompassing group for the zoom
                    var g = svg.append("g")
                        .attr("class", "everything");

                    //draw circles for the nodes
                    var node = g.selectAll('.nodes')
                        .data(graph.nodes)
                        .enter()
                        .append('g')
                        .attr('class', 'nodes');

                    node.each(function (singleNode) {
                        if (singleNode.isTopic == 1) {
                            var percentage = []
                            var sum = sumRatiosPolitician(singleNode, firstSelected, secondSelected)
                            if (sum > 0) {
                                percentage.push({ "politic": firstSelected, "percent": Math.round(singleNode.politicians[firstSelected]["ratio"] / sum * 100), "color": firstColor })
                                percentage.push({ "politic": secondSelected, "percent": Math.round(singleNode.politicians[secondSelected]["ratio"] / sum * 100), "color": secondColor })

                                NodePieBuilder.drawNodePie(d3.select(this), percentage, {
                                    parentNodeColor: "#FFFF00",
                                    outerStrokeWidth: 30,
                                    radius: fromSumToSize(sum),
                                    showLabelText: true,
                                    labelText: singleNode.id,
                                    labelColor: "blue"
                                });
                            }
                            var nodeEnter = d3.select(this);
                            nodeEnter.on("click", function (clickedNode) {
                                document.getElementById("leftTweetContainer").classList.remove("d-none");
                                document.getElementById("rightTweetContainer").classList.remove("d-none");
                                cleanTwitterEnbeddedProfiles();
                                cleanTwitterEnbeddedTweets();
                                var numberTweets = 5;
                                document.getElementById("leftTweetsPoliticianContainer").innerHTML = "Tweets in which " + firstSelected + " deals with the topic " + clickedNode.id + ": <br>"
                                document.getElementById("rightTweetsPoliticianContainer").innerHTML = "Tweets in which " + secondSelected + " deals with the topic " + clickedNode.id + ": <br>"
                                for (var i = 0; i < numberTweets; i++) {
                                    twttr.widgets.createTweet(
                                        clickedNode.politicians[firstSelected]["tweet_ids"][i],
                                        document.getElementById("leftTweetsPoliticianContainer"),
                                        {
                                            width: widthCard * 0.3,
                                            height: '700'
                                        }).then(function (el) {
                                            console.log('Embedded a timeline.')
                                        }).catch(function (err) {
                                            console.log("Error in embedding tweet. ID = " + clickedNode.politicians[firstSelected]["tweet_ids"][i]);
                                            console.log(err);
                                        });
                                    twttr.widgets.createTweet(
                                        clickedNode.politicians[secondSelected]["tweet_ids"][i],
                                        document.getElementById("rightTweetsPoliticianContainer"),
                                        {
                                            width: widthCard * 0.3,
                                            height: '700'
                                        }).then(function (el) {
                                            console.log('Embedded a timeline.')
                                        }).catch(function (err) {
                                            console.log("Error in embedding tweet. ID = " + clickedNode.politicians[secondSelected]["tweet_ids"][i]);
                                            console.log(err);
                                        });
                                }
                            })
                            //Possible interactions
                            /*nodeEnter.on('mouseenter', function (d) {
                                // select element in current context
                                console.log(d)
                                console.log(d3.select(this))
                                d3.select(this)
                                    .transition()
                                    .attr("transform","scale(4)");
                            })
                            // set back
                            nodeEnter.on('mouseleave', function () {
                                console.log('mouseleave')
                                d3.select(this)
                                    .transition()
                                    .attr("transform","scale("+fromSumToSize(sum)/2+","+fromSumToSize(sum)/2+",-4)");
                            });*/

                        }
                        else {
                            //Not topics so photo of politician
                            var nodeEnter = d3.select(this);
                            nodeEnter.append("circle")
                                .attr("r", imageRadius + 10)
                                .attr("cx", imageRadius / 2)
                                .attr("cy", imageRadius / 2)
                                .attr("fill", function (d) {
                                    if (d.side == "left") {
                                        return objectPoliticians[firstSelected].color
                                    }
                                    else {
                                        return objectPoliticians[secondSelected].color
                                    }
                                })

                            nodeEnter.append("circle")
                                .attr("r", imageRadius / 1.5)
                                .attr("cx", function (d) {
                                    if (d.side == "left") {
                                        return imageRadius * 1.1
                                    }
                                    else {
                                        return -imageRadius * 0.1
                                    }
                                })
                                .attr("cy", imageRadius / 2)
                                .attr("fill", function (d) {
                                    if (d.side == "left") {
                                        return firstColor
                                    }
                                    else {
                                        return secondColor
                                    }
                                })

                            nodeEnter.append("svg:image")
                                .attr("xlink:href", function (d) {
                                    if (d.side == "left") {
                                        return objectPoliticians[firstSelected].photo;
                                    }
                                    else {
                                        return objectPoliticians[secondSelected].photo
                                    }
                                })
                                .attr("clip-path", "url(#clipCircle)")
                                .attr("x", function (d) { return -imageRadius / 2 - 45 })
                                .attr("y", function (d) { return -imageRadius / 2 })
                                .attr("height", imageRadius * 3)
                                .attr("width", imageRadius * 3.1)

                            nodeEnter.append("text")
                                .text(function (d) { return (d.id) })
                                .attr("fill", function (d) { return (d.color) })
                                .attr("dy", imageRadius * 1.9);

                            nodeEnter.on("click",
                                function (clickedNode) {
                                    cleanTwitterEnbeddedTweets();
                                    if (clickedNode.id == firstSelected) {
                                        document.getElementById("leftTweetContainer").classList.remove("d-none");
                                        if (document.getElementById("rightProfilePoliticianContainer").innerHTML == "") {
                                            document.getElementById("rightTweetContainer").classList.add("d-none");
                                        }
                                        document.getElementById("leftProfilePoliticianContainer").innerHTML = "Twitter timeline of " + firstSelected + ": <br>"
                                        twttr.widgets.createTimeline(
                                            {
                                                sourceType: 'profile',
                                                screenName: objectPoliticians[firstSelected]["twetterName"]
                                            },
                                            document.getElementById("leftProfilePoliticianContainer"),
                                            {
                                                width: widthCard * 0.3,
                                                height: '700'
                                            }).then(function (el) {
                                                console.log('Embedded a timeline.')
                                            }).catch(function (err) {
                                                console.log("Error in embedding timeline of " + firstSelected)
                                                console.log(err)
                                            });
                                    }
                                    else {
                                        document.getElementById("rightTweetContainer").classList.remove("d-none");
                                        if (document.getElementById("leftProfilePoliticianContainer").innerHTML == "") {
                                            document.getElementById("leftTweetContainer").classList.add("d-none");
                                        }
                                        document.getElementById("rightProfilePoliticianContainer").innerHTML = "Twitter timeline of " + secondSelected + ": <br>"
                                        twttr.widgets.createTimeline(
                                            {
                                                sourceType: 'profile',
                                                screenName: objectPoliticians[secondSelected]["twetterName"]
                                            },
                                            document.getElementById("rightProfilePoliticianContainer"),
                                            {
                                                width: widthCard * 0.3,
                                                height: '700'
                                            }).then(function (el) {
                                                console.log('Embedded a timeline.')
                                            }).catch(function (err) {
                                                console.log("Error in embedding timeline of " + secondSelected)
                                                console.log(err)
                                            });
                                    }
                                }
                            )
                        }
                    });

                    //add drag capabilities
                    var drag_handler = d3.drag()
                        .on("start", drag_start)
                        .on("drag", drag_drag)
                        .on("end", drag_end);

                    drag_handler(node);


                    //add zoom capabilities
                    var zoom_handler = d3.zoom()
                        .on("zoom", zoom_actions);

                    zoom_handler(svg);

                    /** Functions **/

                    //Drag functions
                    //d is the node
                    function drag_start(d) {
                        if (!d3.event.active) simulation.alphaTarget(0.01).restart();
                        d.fx = d.x;
                        d.fy = d.y;
                    }

                    //make sure you can't drag the circle outside the box
                    function drag_drag(d) {
                        d.fx = d3.event.x;
                        d.fy = d3.event.y;
                    }

                    function drag_end(d) {
                        if (!d3.event.active) simulation.alphaTarget(0.01);
                        d.fx = null;
                        d.fy = null;
                    }

                    //Zoom functions
                    function zoom_actions() {
                        //Zoom limits
                        if (d3.event.transform.k < 1.5) {
                            if (d3.event.transform.k > 0.5) {
                                g.attr("transform", d3.event.transform)
                            }
                            else {
                                d3.event.transform.k = 0.51
                            }

                        }
                        else {
                            d3.event.transform.k = 1.49
                        }
                    }

                    function tickActions() {
                        //update circle positions each tick of the simulation
                        node.attr('transform', d => `translate(${d.x},${d.y})`);
                    }
                    document.getElementById("primaryButton").disabled = true;
                    document.getElementById("cancelButton").disabled = false;
                })
                    .catch(function (error) {
                        console.log("ERROR!", error)
                    });
            }
            else {
                if (firstSelected == "--") {
                    firstPoliticiansSelect.classList.add("is-invalid")
                }
                if (secondSelected == "--") {
                    secondPoliticiansSelect.classList.add("is-invalid")
                }
            }
        }

        var cancelButton = document.getElementById("cancelButton")

        cancelButton.onclick = function () {
            //Initial state
            document.getElementById("svg").innerHTML = ""
            document.getElementById("card").classList.add("d-none");
            document.getElementById("leftTweetContainer").classList.add("d-none");
            document.getElementById("rightTweetContainer").classList.add("d-none");
            document.getElementById("primaryButton").disabled = false;
            document.getElementById("cancelButton").disabled = true;
            cleanTwitterEnbeddedTweets();
            cleanTwitterEnbeddedProfiles();
        }

    });