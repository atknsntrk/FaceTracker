function setup() 
{
    createCanvas(1280,720);
    background(255);

    const ws = new WebSocket("ws://localhost:8000/ws");

    ws.onmessage = function(event) {
        let data = JSON.parse(event.data)


        background(255)
        if(data["emotion"] == 'happy') {
            fill(color(0,255,0))
        } else if (data["emotion"] == 'sad'){
            fill(color(0,0,255))
        } else {
            fill(color((255,255,255)))
        }

        circle(data['x']+(data['w']/2), data['y']+(data['h']/2), data['w']/2)


    }
}

function draw()
{

}