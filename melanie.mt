def even(x) { 
    answer = false;
    div2 = x/2;
    times2 = div2*2;
    if (times2 == x) {
        answer = true;
  }
  else {
    answer = false;
  }
  return answer;
}

def main() {

map = FlatMap("xmap", 300, 300, 100);

for (x=0; x < 300; x = x+1) {
    for (y=0; y < 300; y = y+1) {
        if ( even(x) ) { 
            p = new Point(x,y,0);
            map.add(block(COBBLESTONE), p);
        }
        else {
            p = new Point(x,y,0);
            map.add(block(BRICK), p);
        }
    }
}  

for (x=0; x < 300; x = x+1) {
    for (y=300; y > 0; y = y-1) {
        if ( even(x) ) { 
            p = new Point(x,y,0);
            map.add(block(COBBLESTONE), p);
        }
        else {
            p = new Point(x,y,0);
            map.add(block(BRICK), p);
        }
    }
}

map.close();
}
