// Desmos graphs for the Unit 2 decks. Every list is from OpenStax Introductory Statistics 2e.
// Paste into the console on https://www.desmos.com/calculator, then run M117.build("2.5").
window.M117 = (function () {
  var op = function (f, a) { return "\\operatorname{" + f + "}\\left(" + a + "\\right)"; };
  var list = function (xs) { return "\\left[" + xs.join(",") + "\\right]"; };
  var rep = function (v, n) {
    return "\\left[" + v + "\\ \\operatorname{for}\\ i=\\left[1..." + n + "\\right]\\right]";
  };

  function Graph() {
    this.items = [];
    this.n = 0;
    this.folder = undefined;
  }
  Graph.prototype.id = function () { return "m" + this.n++; };
  Graph.prototype.text = function (t) {
    this.items.push({ type: "text", id: this.id(), text: t, folderId: this.folder });
  };
  Graph.prototype.open = function (title, collapsed) {
    this.folder = this.id();
    this.items.push({ type: "folder", id: this.folder, title: title, collapsed: !!collapsed });
  };
  Graph.prototype.close = function () { this.folder = undefined; };
  Graph.prototype.ex = function (latex, extra) {
    var e = { type: "expression", id: this.id(), latex: latex, folderId: this.folder, color: "#2a6f7a" };
    for (var k in extra || {}) e[k] = extra[k];
    this.items.push(e);
  };
  Graph.prototype.five = function (v) {
    this.ex(op("min", v));
    this.ex(op("quartile", v + ",1"));
    this.ex(op("median", v));
    this.ex(op("quartile", v + ",3"));
    this.ex(op("max", v));
  };
  Graph.prototype.fences = function (v, name) {
    this.ex(name + "=" + op("quartile", v + ",3") + "-" + op("quartile", v + ",1"));
    this.ex(op("quartile", v + ",1") + "-1.5" + name);
    this.ex(op("quartile", v + ",3") + "+1.5" + name);
  };

  var FOURTEEN = [1, 11.5, 6, 7.2, 4, 8, 9, 10, 6.8, 8.3, 2, 2, 10, 1];

  var specs = {
    "2.2": function (g) {
      g.text("MATH 117 · 2.2 Histograms. The book prints the counts, not the 100 heights, so each list below repeats a bar's label that many times. histogram( ) draws it. Change the bin width and the shape changes.");
      g.open("Example 2.7 · 100 soccer players, heights in inches");
      g.text("Bar labels and counts from the slide: 60 (5), 62 (3), 64 (15), 66 (40), 68 (17), 70 (12), 72 (7), 74 (1).");
      g.ex("H=" + op("join", [rep(60, 5), rep(62, 3), rep(64, 15), rep(66, 40), rep(68, 17), rep(70, 12), rep(72, 7), rep(74, 1)].join(",")));
      g.ex(op("length", "H"));
      g.ex(op("histogram", "H,2"));
      g.text("The book's bars are 2 inches wide, starting at 59.95. Desmos places its own edges, so compare the counts, not the edges.");
      g.close();
      g.open("Example 2.8 · books bought by 50 students", true);
      g.text("Counts: 1 book (11), 2 (10), 3 (16), 4 (6), 5 (5), 6 (2).");
      g.ex("K=" + op("join", [rep(1, 11), rep(2, 10), rep(3, 16), rep(4, 6), rep(5, 5), rep(6, 2)].join(",")));
      g.ex(op("length", "K"));
      g.ex(op("histogram", "K,1"), { hidden: true });
      g.text("Turn the histogram on. The bar for 3 runs from 2.5 to 3.5 in the book, and 16 of the 50 bought three books.");
      g.close();
      return { left: 58, right: 76, bottom: -5, top: 50 };
    },
    "2.3": function (g) {
      g.text("MATH 117 · 2.3 Quartiles and percentiles. Every list is from OpenStax Introductory Statistics 2e. Open a folder and change any number.");
      g.open("Warm-up · the 14 values");
      g.ex("V=" + list(FOURTEEN));
      g.ex(op("sort", "V"));
      g.five("V");
      g.text("The book's Q1 and Q3 are the medians of the two halves. Desmos quartile( ) matches: 2 and 9.");
      g.close();
      g.open("Example 2.16 · 29 ordered ages · percentiles", true);
      g.ex("G=" + list([18, 21, 22, 25, 26, 27, 29, 30, 31, 33, 36, 37, 41, 42, 47, 52, 55, 57, 58, 62, 64, 67, 69, 71, 72, 73, 74, 76, 77]));
      g.text("The book's rule: i = (k/100)(n + 1). If i is not whole, average the ages on each side. Drag k.");
      g.ex("k=70", { sliderBounds: { min: "4", max: "96", step: "1" } });
      g.ex("i=\\frac{k}{100}\\left(" + op("length", "G") + "+1\\right)");
      g.ex("\\frac{G\\left[\\operatorname{floor}\\left(i\\right)\\right]+G\\left[\\operatorname{ceil}\\left(i\\right)\\right]}{2}");
      g.text("Do not use Desmos quantile( ) here. It uses a different percentile rule than the book.");
      g.close();
      g.open("Example 2.13 · 13 house prices", true);
      g.ex("H=" + list([114950, 158000, 230500, 387000, 389950, 479000, 488800, 529000, 575000, 639000, 659000, 1095000, 5500000]));
      g.five("H");
      g.fences("H", "R_{H}");
      g.close();
      g.open("Try It 2.13 · 11 salaries", true);
      g.ex("S=" + list([28000, 33000, 40500, 42000, 54000, 54000, 64500, 68500, 69000, 72000, 120000]));
      g.five("S");
      g.fences("S", "R_{S}");
      g.close();
      return { left: -1, right: 13, bottom: -2, top: 4 };
    },
    "2.4": function (g) {
      g.text("MATH 117 · 2.4 Box plots. Every list is from OpenStax Introductory Statistics 2e. Change a number and watch the box move.");
      g.open("The 14 values");
      g.ex("V=" + list(FOURTEEN));
      g.five("V");
      g.ex("R_{V}=" + op("quartile", "V,3") + "-" + op("quartile", "V,1"));
      g.ex(op("boxplot", "V"));
      g.close();
      g.open("Try It 2.22 · 10 project times, in hours", true);
      g.ex("P=" + list([2, 3, 5, 3, 4, 4, 3, 11, 3, 2]));
      g.five("P");
      g.fences("P", "R_{P}");
      g.ex(op("boxplot", "P"), { hidden: true });
      g.text("Turn on the box plot above. Try changing 11 to 5: is it still past the fence?");
      g.close();
      return { left: -1, right: 13, bottom: -2, top: 4 };
    },
    "2.5": function (g) {
      g.text("MATH 117 · 2.5 Center. Every list is from OpenStax Introductory Statistics 2e. Open a folder and change any number.");
      g.open("Example 2.26 · 40 patient ages");
      g.ex("A=" + list([3, 4, 8, 8, 10, 11, 12, 13, 14, 15, 15, 16, 16, 17, 17, 18, 21, 22, 22, 24, 24, 25, 26, 26, 27, 27, 29, 29, 31, 32, 33, 33, 34, 34, 35, 37, 40, 44, 44, 47]));
      g.ex(op("length", "A"));
      g.ex(op("mean", "A"));
      g.ex(op("median", "A"));
      g.ex(op("dotplot", "A"));
      g.close();
      g.open("Example 2.27 · 50 incomes in a town", true);
      g.text("49 people earn $30,000. One person earns b. Drag b: the mean follows it, the median does not.");
      g.ex("b=5000000", { sliderBounds: { min: "30000", max: "5000000", step: "10000" } });
      g.ex("I=" + op("join", rep(30000, 49) + ",b"));
      g.ex(op("mean", "I"));
      g.ex(op("median", "I"));
      g.close();
      g.open("Try It 2.27 · 60 houses", true);
      g.text("29 houses at $280,000, 30 at $315,000, and one at $2,500,000.");
      g.ex("H=" + op("join", rep(280000, 29) + "," + rep(315000, 30) + ",\\left[2500000\\right]"));
      g.ex(op("length", "H"));
      g.ex(op("mean", "H"));
      g.ex(op("median", "H"));
      g.close();
      g.open("Example 2.28 · 20 scores", true);
      g.ex("S=" + list([50, 53, 59, 59, 63, 63, 72, 72, 72, 72, 72, 76, 78, 81, 83, 84, 84, 84, 90, 93]));
      g.ex(op("mean", "S"));
      g.ex(op("median", "S"));
      g.text("Desmos has no mode command. Count by eye: 72 appears five times, so the mode is 72.");
      g.close();
      return { left: -2, right: 52, bottom: -1, top: 8 };
    },
    "2.6": function (g) {
      g.text("MATH 117 · 2.6 Skewness. Every list is from OpenStax Introductory Statistics 2e. Compare the mean and the median in each folder.");
      g.open("Warm-up · three lists");
      g.ex("L_{1}=" + list([4, 5, 6, 6, 6, 7, 7, 7, 7, 7, 7, 8, 8, 8, 9, 10]));
      g.ex(op("mean", "L_{1}"));
      g.ex(op("median", "L_{1}"));
      g.ex("L_{2}=" + list([4, 5, 6, 6, 6, 7, 7, 7, 7, 8]));
      g.ex(op("mean", "L_{2}"));
      g.ex(op("median", "L_{2}"));
      g.ex("L_{3}=" + list([6, 7, 7, 7, 7, 8, 8, 8, 9, 10]));
      g.ex(op("mean", "L_{3}"));
      g.ex(op("median", "L_{3}"));
      g.close();
      g.open("Example 2.31 · Terry, Davis, Maris", true);
      g.ex("T=" + list([7, 9, 3, 3, 3, 4, 1, 3, 2, 2]));
      g.ex(op("mean", "T"));
      g.ex(op("median", "T"));
      g.ex("D=" + list([3, 3, 3, 4, 1, 4, 3, 2, 3, 1]));
      g.ex(op("mean", "D"));
      g.ex(op("median", "D"));
      g.ex("M=" + list([2, 3, 4, 4, 4, 6, 6, 6, 8, 3]));
      g.ex(op("mean", "M"));
      g.ex(op("median", "M"));
      g.text("Try it: change Terry's 9 to 30. Which center moves more?");
      g.close();
      return { left: -1, right: 12, bottom: -1, top: 6 };
    },
    "2.7": function (g) {
      g.text("MATH 117 · 2.7 Standard deviation. Every list is from OpenStax Introductory Statistics 2e. stdev( ) is the sample standard deviation s. stdevp( ) is the population σ.");
      g.open("Example 2.32 · 20 fifth-graders, a sample");
      g.text("Ages: 9 once, 9.5 twice, 10 four times, 10.5 four times, 11 six times, 11.5 three times.");
      g.ex("F=" + op("join", "\\left[9\\right]," + rep(9.5, 2) + "," + rep(10, 4) + "," + rep(10.5, 4) + "," + rep(11, 6) + "," + rep(11.5, 3)));
      g.ex(op("length", "F"));
      g.ex(op("mean", "F"));
      g.ex(op("stdev", "F"));
      g.close();
      g.open("Example 2.33 · 31 exam scores", true);
      g.ex("E=" + list([33, 42, 49, 49, 53, 55, 55, 61, 63, 67, 68, 68, 69, 69, 72, 73, 74, 78, 80, 83, 88, 88, 88, 90, 92, 94, 94, 94, 94, 96, 100]));
      g.ex(op("mean", "E"));
      g.ex(op("median", "E"));
      g.ex(op("stdev", "E"));
      g.ex(op("quartile", "E,1"));
      g.ex(op("quartile", "E,3"));
      g.close();
      g.open("Try It 2.32 · 25 baseball ages", true);
      g.ex("B=" + list([21, 21, 22, 23, 24, 24, 25, 25, 28, 29, 29, 31, 32, 33, 33, 34, 35, 36, 36, 36, 36, 38, 38, 38, 40]));
      g.ex(op("mean", "B"));
      g.ex(op("stdev", "B"));
      g.text("Two standard deviations above the mean:");
      g.ex(op("mean", "B") + "+2" + op("stdev", "B"));
      g.close();
      return { left: 8, right: 12.5, bottom: -1, top: 8 };
    },
  };

  return {
    build: function (section) {
      var g = new Graph();
      var bounds = specs[section](g);
      Calc.setBlank();
      Calc.setExpressions(g.items);
      Calc.setMathBounds(bounds);
      return g.items.length;
    },
    sections: Object.keys(specs),
  };
})();
