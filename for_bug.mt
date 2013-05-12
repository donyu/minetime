
def main() {
    map = new Flatmap("xmap_fix", 300, 127, 100);
    for (x = 1; x < 100; x = x + 1) {
        for (y = 1; y < 100; y = y + 1) {
            p = new Point(x, y, 0);
            map.add(block(COBBLESTONE), p);
        }
    } 

    for (x = 1; x < 100; x = x + 1) {
        p1 = new Point(x, x, 0);

        map.add(block(BRICK), p1);
    }

    for (x = 1; x < 200; x = x + 1) {
        y = 1;
    }

    map.close();
}
