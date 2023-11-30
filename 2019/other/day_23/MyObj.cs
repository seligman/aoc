using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DrawNetwork
{
    class MyObj
    {
        public string Name;
        public double Xa;
        public double Ya;
        public double Xb;
        public double Yb;
        public int Framea;
        public int Frameb;
        public int Type;

        public double X(int frame)
        {
            if (Framea == -1)
            {
                return Xa;
            }
            var perc = ((double)(frame - Framea)) / ((double)(Frameb - Framea));
            return Xa * (1.0 - perc) + Xb * perc;
        }

        public double Y(int frame)
        {
            if (Framea == -1)
            {
                return Ya;
            }
            var perc = ((double)(frame - Framea)) / ((double)(Frameb - Framea));
            return Ya * (1.0 - perc) + Yb * perc;
        }

        public bool IsVisible(int frame)
        {
            if (Framea == -1)
            {
                return true;
            }
            if (frame >= Framea && frame < Frameb)
            {
                return true;
            }
            return false;
        }
    }
}
