using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace DrawNetwork
{
    public partial class NetworkForm : Form
    {
        public NetworkForm()
        {
            InitializeComponent();
        }

        private void NetworkForm_Load(object sender, EventArgs e)
        {
            ClientSize = new Size(600, 600);
            SetupAll();

            var img = new Bitmap(600, 600, System.Drawing.Imaging.PixelFormat.Format32bppArgb);
            using (var g = Graphics.FromImage(img))
            {
                g.SmoothingMode = System.Drawing.Drawing2D.SmoothingMode.HighQuality;
                g.CompositingQuality = System.Drawing.Drawing2D.CompositingQuality.HighQuality;
                g.InterpolationMode = System.Drawing.Drawing2D.InterpolationMode.HighQualityBicubic;
                for (frame = 0; frame < maxf; frame++)
                {
                    DrawFrame(g);
                    img.Save("frame_" + frame.ToString("00000") + ".png");
                }
            }
        }

        private void NetworkForm_Paint(object sender, PaintEventArgs e)
        {
            DrawFrame(e.Graphics);
        }

        List<MyObj> objs = new List<MyObj>();
        int frame = 0;
        int maxf = 0;

        void SetupAll()
        {
            for (int i = 0; i < 50; i++)
            {
                var x = -Math.Sin(((double)i) / 50.0 * Math.PI * 2.0 + Math.PI) * 275.0 + 300.0;
                var y = Math.Cos(((double)i) / 50.0 * Math.PI * 2.0 + Math.PI) * 275.0 + 300.0;
                var temp = new MyObj();
                temp.Xa = x;
                temp.Ya = y;
                temp.Name = i.ToString();
                temp.Framea = -1;
                temp.Type = 1;
                objs.Add(temp);
            }

            {
                var temp = new MyObj();
                temp.Xa = 575.0;
                temp.Ya = 25.0;
                temp.Name = "N";
                temp.Framea = -1;
                temp.Type = 1;
                objs.Add(temp);
            }

            int dur = 20;
            int off = -dur;
            var offs = new Dictionary<int, int>();
            var sent = new Dictionary<int, int>();
            using (var sr = new StreamReader(@"traffic.txt"))
            {
                while (!sr.EndOfStream)
                {
                    var line = sr.ReadLine();
                    var vals = line.Split(',');
                    int frame = int.Parse(vals[0]);
                    if (!offs.ContainsKey(frame))
                    {
                        off += dur;
                        offs[frame] = off;
                    }
                }
            }

            using (var sr = new StreamReader(@"traffic.txt"))
            {
                int last = -1;

                while (!sr.EndOfStream)
                {
                    var line = sr.ReadLine();
                    var vals = line.Split(',');
                    var temp = new MyObj();
                    int frame = int.Parse(vals[0]);
                    int src = int.Parse(vals[1]);
                    int dest = int.Parse(vals[2]);
                    if (dest == 255)
                    {
                        dest = 50;
                    }
                    if (src == 255)
                    {
                        src = 50;
                    }

                    if (last != frame)
                    {
                        last = frame;
                        sent = new Dictionary<int, int>();
                    }
                    if (!sent.ContainsKey(src))
                    {
                        sent[src] = 0;
                    }
                    else
                    {
                        sent[src] += 1;
                    }

                    temp.Xa = objs[src].Xa;
                    temp.Ya = objs[src].Ya;
                    temp.Xb = objs[dest].Xa;
                    temp.Yb = objs[dest].Ya;
                    temp.Framea = offs[frame] + sent[src];
                    temp.Frameb = offs[frame] + dur + sent[src];
                    temp.Type = 2;
                    temp.Name = "";
                    objs.Add(temp);
                    maxf = Math.Max(temp.Frameb + 30, maxf);
                }
            }
        }

        void DrawFrame(Graphics g)
        {
            g.Clear(Color.Black);

            using (var fnt = new Font("Courier", 10, FontStyle.Bold))
            using (var bb = new SolidBrush(Color.FromArgb(255, 128, 128)))
            {
                foreach (var obj in objs)
                {
                    if (obj.IsVisible(frame))
                    {
                        int size = 24;
                        var clr = Brushes.White;
                        if (obj.Type == 2)
                        {
                            size = 20;
                            clr = bb;
                        }
                        g.FillEllipse(clr, (int)obj.X(frame) - size / 2, (int)obj.Y(frame) - size / 2, size, size);
                        var sf = (StringFormat)StringFormat.GenericDefault.Clone();
                        sf.Alignment = StringAlignment.Center;
                        sf.LineAlignment = StringAlignment.Center;

                        g.DrawString(obj.Name, fnt, Brushes.Black, new Rectangle((int)obj.X(frame) - 15, (int)obj.Y(frame) - 15, 30, 30), sf);
                    }
                }
            }
        }

        private void timer1_Tick(object sender, EventArgs e)
        {
            frame++;
            if (frame > maxf)
            {
                frame = 0;
            }
            Invalidate();
        }
    }
}
